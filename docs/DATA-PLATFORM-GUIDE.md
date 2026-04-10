---
title: Data Platform Guide
---

# Data Platform Guide (Fabric & Databricks)

This guide covers platform-specific patterns, cluster setup, and optimization for Microsoft Fabric and Databricks.

**SETUP REQUIRED**: Customize this for your chosen platform (Fabric, Databricks, or both equally).

---

## Quick Decision Matrix

| Scenario | Fabric | Databricks | Notes |
|----------|--------|-----------|-------|
| **Storage** | Lakehouse (managed Delta) | Delta Lake (flexible) | Fabric simpler, Databricks more control |
| **Compute** | Capacity (autoscale) | Cluster (user-managed) | Fabric "pay per compute", Databricks "pay per DBU" |
| **Auth** | AAD/MSA integration | API tokens/service principals | Fabric integrated with Microsoft ecosystem |
| **SQL** | Fabric SQL editor | Databricks SQL | Very similar dialects |
| **Admin** | Workspace admin | Admin console | Fabric simpler governance |
| **Secrets** | Workspace secrets | Databricks secrets scope | Different API, same purpose |
| **Migration** | From Power BI, Excel | From other cloud platforms | Consider where your data starts |

---

## Setup: Choosing Your Platform

### If You're Fabric-First
- Existing Microsoft 365 investment? → Fabric
- Power BI already deployed? → Fabric
- Work primarily in Azure? → Either (Databricks more costly)

### If You're Databricks-First
- Multi-cloud strategy? → Databricks (AWS, Azure, GCP)
- Advanced ML workflows? → Databricks
- Existing Databricks investment? → Databricks

### If You're Using Both
- Reference both sections below
- Platform-specific code in `examples/` folders per skill
- Configuration in `Data-PLATFORM-GUIDE.md` per project

---

## Microsoft Fabric Setup

### Workspaces & Lakehouses

```python
# Access Lakehouse in Fabric notebook
from notebookutils import mssparkutils

# Your lakehouse is at: /Workspace/lakehouse_name/Files/
lakehouse_path = "/Workspace/my_lakehouse/Files/data/"

# Read from Lakehouse
df = spark.read.parquet(f"{lakehouse_path}orders.parquet")

# Write to Lakehouse (creates Delta table automatically)
df.write.mode("overwrite").parquet(f"{lakehouse_path}processed/")

# Or use SQL
spark.sql("""
    CREATE TABLE orders_processed AS
    SELECT * FROM parquet.`/Workspace/my_lakehouse/Files/data/processed/`
""")
```

### Secrets in Fabric

```python
from notebookutils.credentials import CredentialBuilder
from pyspark.databricks.sql import SparkSession

# Create credentials
creds = CredentialBuilder().build()

# Use in connection string
db_url = f"jdbc:sqlserver://{host}:1433"
db_user = creds.get("username")  # Or use Fabric Secrets
db_pass = creds.get("password")

# Read from external database
df = spark.read \
    .format("jdbc") \
    .option("url", db_url) \
    .option("dbtable", "orders") \
    .option("user", db_user) \
    .option("password", db_pass) \
    .load()
```

### Capacity Planning (Fabric)

```
Capacity unit (CU) sizing:
- Trial / Dev: F2 (2 CU) → ~$1/hour
- Small pipeline: F4 (4 CU) → ~$2/hour
- Production: F64 (64 CU) → ~$30/hour

Cost = CU count × $1.50/hour (US pricing, varies by region)

Scaling: Increase CU to handle more concurrent jobs
```

---

## Databricks Setup

### Cluster Configuration

**Recommended for Data Engineering** (adjust for your workload):

```json
{
  "cluster_name": "data-eng-cluster",
  "spark_version": "13.3.x-scala2.12",
  "node_type_id": "i3.xlarge",
  "num_workers": 4,
  "autoscale": {
    "min_workers": 2,
    "max_workers": 8
  },
  "spark_conf": {
    "spark.sql.adaptive.enabled": "true",
    "spark.sql.shuffle.partitions": "auto",
    "spark.databricks.io.cache.enabled": "true",
    "spark.databricks.delta.preview.enabled": "true"
  },
  "init_scripts": [
    {
      "dbfs": {
        "destination": "dbfs:/init-scripts/setup.sh"
      }
    }
  ]
}
```

**Startup time**: ~1 min (small), ~5 min (large)  
**Cost**: Based on DBU (Databricks Unit) consumption

### Secrets in Databricks

```python
import dbutils

# Create secret scope (one-time in admin CLI)
# databricks secrets create-scope --scope my-scope

# Store secret
# databricks secrets put --scope my-scope --key db-password --string-value "..."

# Use in notebook
db_password = dbutils.secrets.get("my-scope", "db-password")
db_user = dbutils.secrets.get("my-scope", "db-user")

# Read from external database
df = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:sqlserver://...") \
    .option("user", db_user) \
    .option("password", db_password) \
    .load()
```

### Jobs & Scheduling

```python
# Run a notebook as a job
result = dbutils.notebook.run(
    path="../pipelines/daily_etl",
    timeout_seconds=3600
)

# Or schedule via UI:
# 1. Create job from Workflows → New Job
# 2. Select notebook
# 3. Set schedule (cron: "0 2 * * *" = 2am daily)
# 4. Set cluster + max concurrent runs
```

---

## Platform-Specific Optimization

### Partitioning (Both)

```python
# Partition by date (most common for time-series data)
df.write \
    .partitionBy("date") \
    .mode("overwrite") \
    .parquet("/mnt/data/orders_partitioned/")

# Query: Only reads relevant date partitions (PRUNING)
result = spark.sql("""
    SELECT * FROM parquet.`/mnt/data/orders_partitioned/`
    WHERE date = '2026-04-09'
""")
# Efficient: Reads only 1 date partition, not all 365 days
```

### Broadcast Joins (Both)

```python
from pyspark.sql.functions import broadcast

# Small table (< 100MB) replicated to all workers = FAST join
large_orders.join(broadcast(small_products), on="product_id")

# vs. SHUFFLE join (slow)
large_orders.join(small_products, on="product_id")  # Don't do this
```

### Caching (Both)

```python
# Cache intermediate results (in memory)
df_processed = complex_transform(df)
df_processed.cache()

# Now multiple operations are faster
count = df_processed.count()
sample = df_processed.limit(100)

# Release when done
df_processed.unpersist()
```

---

## Column Pruning Optimization

### Automatic in Spark

```python
# Spark automatically reads only needed columns (Parquet format)
result = spark.sql("""
    SELECT id, amount FROM large_table  -- Only 2 columns read
""")

# vs. BAD: Reads entire table, then selects
df = spark.sql("SELECT * FROM large_table")
df = df.select("id", "amount")  # Selects after reading (wasteful)
```

---

## Testing Platform-Specific Code

### Fabric

```python
# tests/test_fabric.py
import pytest
from notebookutils import mssparkutils

def test_lakehouse_read(spark):
    """Test reading from Lakehouse."""
    path = "/Workspace/test-lakehouse/Files/"
    df = spark.read.parquet(f"{path}test_data.parquet")
    assert df.count() > 0
```

### Databricks

```python
# tests/test_databricks.py
import pytest
import dbutils

def test_secret_access():
    """Test secret retrieval."""
    secret = dbutils.secrets.get("test-scope", "test-key")
    assert secret is not None

def test_unity_catalog():
    """Test Unity Catalog access."""
    df = spark.sql("SELECT * FROM catalog.schema.table LIMIT 1")
    assert df.count() > 0
```

---

## Migration Between Platforms

### Fabric → Databricks

```python
# Fabric:
df = spark.sql("SELECT * FROM catalog.schema.table")

# Databricks (Unity Catalog):
df = spark.sql("SELECT * FROM catalog.schema.table")  # Same!

# Databricks (non-Unity):
df = spark.sql("SELECT * FROM default.table")
```

### Common Gotchas

| Issue | Symptom | Fix |
|-------|---------|-----|
| Path differences | FileNotFoundError | Use platform-specific paths (`/Workspace/` vs `/mnt/`) |
| Secret scope mismatch | SecretNotFound | Check secret scope name |
| Cluster not running | Jobs timeout without error | Auto-start cluster or pre-warm |
| Memory OOM | "Out of memory" | Reduce worker count, increase memory config |

---

## Performance Benchmarking

```python
import time

# Fabric/Databricks
start = time.time()
result = spark.sql("SELECT COUNT(*) FROM large_table")
result.show()  # Trigger execution
elapsed = time.time() - start

print(f"Query took {elapsed:.2f} seconds")
```

---

## Further Reading

- [Microsoft Fabric Documentation](https://learn.microsoft.com/en-us/fabric/)
- [Databricks Best Practices](https://docs.databricks.com/en/)
- [Delta Lake](https://delta.io/)
- [Apache Spark Tuning](https://spark.apache.org/docs/latest/tuning.html)

---

## Customization

Edit this file to add:
- Your workspace names
- Cluster configurations (copy-paste from your Databricks admin)
- Common paths in your Lakehouse
- Team-specific performance tips
- Links to internal runbooks
