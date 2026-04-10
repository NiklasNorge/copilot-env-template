---
name: fabric-and-databricks.instructions
description: Auto-loads when you open files in Microsoft Fabric or Databricks notebooks. Guidance on Python runtime (recommended for cost) and Polars for data processing.
---

# Fabric & Databricks Specifics

## ⚡ Runtime Choice: Python vs Spark (Cost Optimization)

**TL;DR**: Use Python runtime + Polars for most workloads (cheaper, simpler).

| Aspect | Python Runtime | Spark Runtime |
|--------|---|---|
| **Cost** | Low (no cluster overhead) | Higher (clusters required) |
| **Speed** | Fast for <10GB | Best for >10GB distributed |
| **Memory** | Limited to single machine | Distributed across workers |
| **Use Case** | ETL, validation, transformations | Large-scale distributed compute |

### When to Use Python Runtime (Recommended)

```python
# ✅ Python runtime: Good for most data eng
import polars as pl

df = pl.read_parquet("/Workspace/data/orders.parquet")
df_clean = df.filter(pl.col("amount") > 0).select(["id", "date", "amount"])
df_clean.write_parquet("/Workspace/data/orders_clean.parquet")
```

**Cost**: ~1-2 cents per notebook run  
**Speed**: Sub-minute for typical transforms

### When to Use Spark Runtime

```python
# Spark: Only if dataset > 50GB or complex distributed joins
df = spark.read.format("delta").table("large_catalog.table")
result = df.groupBy("region").agg({"sales": "sum"})
result.write.saveAsTable("aggregated_sales")
```

**Cost**: $0.30-$1.00+ per cluster-hour  
**Speed**: Best for massive datasets

---

## Platform Overview

| Aspect | Fabric | Databricks | Notes |
|--------|--------|-----------|-------|
| **Storage** | Lakehouse (Delta Lake) | Delta Lake | Same underlying format |
| **Cluster** | Capacity-based (autoscale) | User-controlled | Fabric simpler, Databricks more control |
| **Secrets** | Workspace secrets | Databricks secrets | Store creds here, not in code |
| **API** | `notebookutils` | `dbutils` | Different but similar |
| **SQL** | Fabric SQL editor | Databricks SQL | Similar SQL dialects |

---

## Common Patterns

### Load Data (Both Platforms)

```python
# Fabric
df = spark.sql("SELECT * FROM catalog.schema.table")

# Databricks
df = spark.read.parquet("/mnt/data/file.parquet")

# Both: Read from Lakehouse
df = spark.read.parquet("/Workspace/path/file.parquet")
```

### Store Data (Both Platforms)

```python
# Write to Lakehouse (managed)
df.write.mode("overwrite").parquet("/Workspace/data/output.parquet")

# Register as table
spark.sql("""
    CREATE TABLE IF NOT EXISTS bronze.orders AS
    SELECT * FROM parquet.`/Workspace/data/output.parquet`
""")
```

### Secrets (Don't Hardcode!)

```python
# Fabric
from notebookutils.credentials import CredentialBuilder
creds = CredentialBuilder().build()
# (Use in connection string)

# Databricks
dbutils.secrets.get("scope_name", "key_name")
# Then in config:
api_key = dbutils.secrets.get("api-scope", "api-key")
```

---

## Optimization: Partitioning

### When to Partition

- Large tables (> 1GB)
- Filtered often by specific column
- Daily/monthly data (partition by date)

### Partition by Date

```python
# Fabric/Databricks
df.write \
    .partitionBy("date") \
    .mode("overwrite") \
    .parquet("/Workspace/orders_partitioned/")

# Query: Only reads relevant partitions (faster)
spark.sql("SELECT * FROM parquet.`/Workspace/orders_partitioned/` WHERE date = '2026-04-09'")
```

---

## Optimization: Broadcast Joins

### Small-to-Large Join

```python
# Without broadcast: SHUFFLE (slow)
orders.join(product_lookup, on="product_id")

# With broadcast: Small table replicated to all workers (FAST)
from pyspark.sql.functions import broadcast

orders.join(broadcast(product_lookup), on="product_id")

# When to use: product_lookup < 100MB
```

---

## Optimization: Caching

### Cache Intermediate Results

```python
# Cache in memory (for reuse)
df_processed = df.transform(step1).transform(step2)
df_processed.cache()

# Now multiple actions on df_processed are faster
count = df_processed.count()
sample = df_processed.limit(10)

# Release cache when done
df_processed.unpersist()
```

---

## Cluster Configuration (Databricks)

### Recommended for Data Engineering

```json
{
  "spark_version": "13.3.x-scala2.12",
  "node_type_id": "i3.xlarge",
  "num_workers": 4,
  "autoscale": {
    "min_workers": 2,
    "max_workers": 8
  },
  "spark_conf": {
    "spark.sql.adaptive.enabled": "true",
    "spark.databricks.io.cache.enabled": "true"
  }
}
```

---

## Column Pruning (Spark)

### Skip Unnecessary Columns

```python
# BAD: Reads entire table
df_all = spark.sql("SELECT * FROM large_table")
result = df_all.select("id", "amount")  # Only these 2 used

# GOOD: Spark automatically pushes down column filter
df = spark.sql("SELECT id, amount FROM large_table")  # Only these read from disk
```

---

## Avoid Collect on Large Data

### ❌ DON'T

```python
# This brings ALL data to driver (crashes on large data)
data = df.collect()
for row in data:
    print(row)
```

### ✅ DO

```python
# Use Spark operations instead
df.show(20)  # Display first 20 rows
df_filtered = df.filter(df["amount"] > 1000)  # Filter in Spark
df_filtered.write.parquet("output.parquet")  # Write in Spark
```

---

## Testing Spark Code

```python
# tests/test_spark_transform.py
def test_discount_applied(spark_session):
    """Test discount transform."""
    df_input = spark_session.createDataFrame(
        [("A", 100.0), ("B", 200.0)],
        ["id", "amount"]
    )
    
    result = calculate_discount(df_input)
    
    assert result.count() == 2
    assert result.select("id").collect()[0][0] == "A"
```

---

## Platform Gotchas

| Gotcha | Symptom | Fix |
|--------|---------|-----|
| Lazy evaluation | Code runs but nothing happens | Call `.show()`, `.count()`, `.write()` to trigger |
| Memory errors | "Out of memory" on `.collect()` | Use Spark operations; avoid collect on large data |
| Path ambiguity | File not found | Use absolute paths; test with `dbutils.fs.ls()` |
| Schema mismatch | Type conversion errors | Define schema explicitly on read |
| Stale cache | Result doesn't match expectation | Call `.unpersist()` or restart cluster |

---

## Related Skills

- **polars-spark-pandas-patterns**: Detailed engine selection and optimization
- **fabric-databricks-python-runtime**: Python-runtime-first platform heuristics
- **data-quality-testing**: Data validation in Spark
- **notebook-as-code**: Organizing Fabric/Databricks notebooks

---

## References

- [Microsoft Fabric Documentation](https://learn.microsoft.com/en-us/fabric/)
- [Databricks Documentation](https://docs.databricks.com/)
- [Delta Lake](https://delta.io/)
- [Apache Spark Tuning](https://spark.apache.org/docs/latest/tuning.html)
