---
name: spark-pandas-best-practices
description: >-
  Data processing optimization: Polars (primary - local & Python runtime), 
  PySpark (for massive distributed datasets), Pandas (legacy/compatibility). 
  Performance patterns, memory efficiency, platform-specific tuning.
---

# Data Processing Best Practices

## TL;DR: Choose Your Tool

- **Polars** (PRIMARY) → Local + Python runtime on Fabric/Databricks | Fast, memory-efficient, modern API
- **Python Runtime** (Fabric/Databricks) → Cheaper than Spark, scales to ~100GB | Use Polars here
- **PySpark** (FALLBACK) → Only for >50GB distributed datasets | Complex, expensive
- **Pandas** (LEGACY) → Only for compatibility or existing code | Avoid for new projects

---

## Quick Decision Tree

```
Dataset size & platform?
├─ Local machine, <10GB → Polars ✅ (primary choice)
├─ Fabric/Databricks Python runtime, <100GB → Polars ✅ (primary choice)
├─ Local, >10GB in memory chunks → Polars + streaming
├─ Distributed >50GB, complex joins → PySpark
└─ Must match existing codebase → Pandas (legacy)

Budget?
├─ Cost-conscious → Polars + Python runtime (pennies per run)
└─ No constraints → Spark (but still slower than Polars)
```

---

## Polars Best Practices (PRIMARY)

### 1. Load & Transform Efficiently

```python
import polars as pl

# ✅ GOOD: Polars streaming (handles >memory datasets)
df = pl.scan_csv("huge_file.csv").filter(
    pl.col("amount") > 100
).select(["id", "date", "amount"]).collect()

# ✅ GOOD: Parquet with predicate pushdown
df = pl.scan_parquet("/Workspace/data/*.parquet").filter(
    pl.col("date") >= "2026-01-01"
).collect()

# ❌ AVOID: Loading entire dataset then filtering
df = pl.read_csv("huge_file.csv")  # Loads all to memory
df_filtered = df.filter(pl.col("amount") > 100)
```

**Why**: Polars applies filters before loading (predicate pushdown) → 10-100x faster.

### 2. Use Expressions (Not apply)

```python
# ❌ SLOW: Row-by-row processing
df = df.with_columns(
    discount_price=pl.col("price").map_elements(lambda x: x * 0.9)
)

# ✅ FAST: Vectorized expression
df = df.with_columns(
    discount_price=(pl.col("price") * 0.9)
)

# ✅ FAST: String operations
df = df.with_columns(
    upper_name=pl.col("name").str.to_uppercase()
)
```

### 3. GroupBy + Aggregation (Vectorized)

```python
# ✅ GOOD: Vectorized groupby
result = df.group_by("region").agg([
    pl.col("sales").sum().alias("total_sales"),
    pl.col("id").count().alias("transaction_count"),
    pl.col("profit").mean().alias("avg_profit")
]).sort("total_sales", descending=True)

# ❌ AVOID: Loop over groups
results = []
for region, group_df in df.group_by("region"):
    results.append({
        "region": region,
        "total": group_df["sales"].sum()
    })
```

### 4. Memory Efficiency

```python
# ✅ GOOD: Specify dtypes on load (avoids inference)
df = pl.read_csv(
    "data.csv",
    dtypes={
        "id": pl.Int32,
        "amount": pl.Float32,
        "date": pl.Date
    }
)

# ✅ GOOD: Use lazy evaluation (doesn't execute immediately)
lazy_df = pl.scan_csv("huge.csv").filter(
    pl.col("status") == "active"
).select(["id", "name"])
result = lazy_df.collect()  # Execute here

# ✅ GOOD: Stream large files in chunks
for chunk in pl.scan_csv("huge.csv").collect_by_batch(10000):
    process(chunk)
```

### 5. Window Functions & Ranking

```python
# ✅ GOOD: Window function for running totals
df = df.with_columns(
    running_total=pl.col("amount").cum_sum().over("date")
)

# ✅ GOOD: Ranking
df = df.with_columns(
    rank=pl.col("sales").rank(method="dense").over("region")
)
```

---

## Python Runtime on Fabric/Databricks

### Best Practices (Cost Optimization)

```python
# Fabric / Databricks Python notebook
import polars as pl

# ✅ Read from Lakehouse
df = pl.read_parquet("/Workspace/data/orders.parquet")

# ✅ Transform with Polars (cheap, fast)
result = df.filter(pl.col("amount") > 100).group_by("region").agg(
    pl.col("amount").sum()
)

# ✅ Write back
result.write_parquet("/Workspace/output/summary.parquet")
```

**Cost**: ~$0.01 per run (vs $0.30-$1.00 for Spark cluster)  
**Speed**: 10-100x faster than equivalent Spark code

### When Python Runtime Isn't Enough

If dataset > 100GB or requires complex distributed joins → Fall back to PySpark.

---

## PySpark Best Practices (FALLBACK for Large Scale)

*Use only if Polars + Python runtime can't handle the dataset.*

### 1. Partitioning Strategy

```python
# ✅ GOOD: Partition by date
df.write.partitionBy("date").parquet("output/sales")

# ✅ GOOD: Coalesce before write (avoid tiny files)
df.coalesce(100).write.partitionBy("date").parquet("output/sales")
```

### 2. Broadcast Joins (Small to Large)

```python
from pyspark.sql.functions import broadcast

# ❌ SLOW: Shuffle both tables
result = df_large.join(df_lookup, on="id")

# ✅ GOOD: Broadcast small table
result = df_large.join(broadcast(df_lookup), on="id")
```

### 3. Cache Selectively

```python
# ✅ GOOD: Cache expensive transforms
df_processed = df.filter(...).join(...).cache()
count = df_processed.count()
result = df_processed.select(...)
df_processed.unpersist()  # Free memory
```

---

## Pandas (LEGACY - Avoid for New Code)

Only use if:
- Integrating with existing Pandas codebase
- Must use scikit-learn or specific Pandas-only library
- Dataset < 1GB and doesn't fit Polars use case

```python
# ✅ If you must use Pandas:
import pandas as pd

# Specify dtypes (faster than inference)
df = pd.read_csv("data.csv", dtype={"id": "int32", "amount": "float32"})

# Vectorize (don't use .apply)
df["discount"] = df["amount"] * 0.9  # Good

# Use .loc[] for conditional updates
df.loc[df["amount"] < 0, "amount"] = 0  # Good
```

---

## Migration Guide

### Pandas → Polars

| Pandas | Polars | Notes |
|--------|--------|-------|
| `df[df["x"] > 5]` | `df.filter(pl.col("x") > 5)` | Explicit filter |
| `df.groupby("col").sum()` | `df.group_by("col").agg(pl.col(...).sum())` | Agg is explicit |
| `df["new"] = df["old"] * 2` | `df.with_columns((pl.col("old") * 2).alias("new"))` | Immutable |
| `df.merge(other, on="id")` | `df.join(other, on="id")` | Same concept |
| `df.to_csv("out.csv")` | `df.write_csv("out.csv")` | Same API |
| `df["col"].apply(lambda x: ...)` | `df.with_columns(pl.col("col").map_elements(...))` | Avoid both |

### PySpark → Polars

| PySpark | Polars | When |
|---------|--------|------|
| `df.filter(col("x") > 5)` | `df.filter(pl.col("x") > 5)` | Single machine ← prefer Polars |
| `df.groupBy("col").sum()` | `df.group_by("col").sum()` | Single machine ← prefer Polars |
| `df.write.parquet(...)` | `df.write_parquet(...)` | Polars also supports parallel write |
| Large joins (broadcast) | Polars handles automatically | Polars smarter about join strategy |

---

## References

- [Polars Documentation](https://docs.pola.rs/)
- [Fabric Python Runtime](https://learn.microsoft.com/en-us/fabric/data-engineering/python-runtime)
- [Databricks Python Runtime](https://docs.databricks.com/en/compute/python/index.html)
- [PySpark Tuning](https://spark.apache.org/docs/latest/sql-performance-tuning.html)
