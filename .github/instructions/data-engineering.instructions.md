---
name: data-engineering.instructions
description: Auto-loads when you open any .py or .ipynb file in src/data/ or src/notebooks/
---

# Data Engineering Standards

## Project-Wide Data Patterns

### Load → Transform → Validate → Store

All pipelines follow this structure:

```python
"""Daily ETL pipeline."""

import pandas as pd
import logging

from src.data.pipelines import load_source, transform, validate
from src.utils import config

logger = logging.getLogger(__name__)

def main():
    """Execute daily ETL."""
    # 1. LOAD
    df = load_source("prod_db", "orders")
    logger.info(f"Loaded {len(df)} rows")
    
    # 2. TRANSFORM
    df_clean = transform(df)
    
    # 3. VALIDATE
    assert validate(df_clean), "Validation failed"
    logger.info("Validation passed")
    
    # 4. STORE
    df_clean.to_parquet("output/orders_processed.parquet")
    logger.info("Pipeline complete")

if __name__ == "__main__":
    main()
```

---

## Data Quality Non-Negotiables

### Inline Assertions

Every pipeline includes these BEFORE transform:

```python
# Check 1: Data exists
assert df.shape[0] > 0, "No data loaded"

# Check 2: Schema
assert set(df.columns) == {"id", "amount", "date"}, "Schema mismatch"

# Check 3: Key columns non-null
assert df[["id", "date"]].isnull().sum().sum() == 0, "Nulls in key columns"

# Check 4: No duplicates (if applicable)
assert df.duplicated(subset=["id"]).sum() == 0, "Duplicate IDs"

# Check 5: Value ranges
assert df["amount"] >= 0, "Negative amounts"

logger.info("All validation checks passed")
```

### Testing Data Quality

```python
# tests/test_pipeline.py
def test_transform_maintains_row_count(sample_orders):
    """Transform should not drop rows unexpectedly."""
    before = len(sample_orders)
    after = len(transform(sample_orders))
    assert after == before

def test_transform_creates_required_columns(sample_orders):
    """Discount column should always be present."""
    result = transform(sample_orders)
    assert "discount" in result.columns
```

---

## Choosing Pandas vs Spark

| Size | Platform | Choice | Reason |
|------|----------|--------|--------|
| < 1 GB | Local | Pandas | Fast, simple |
| 1-10 GB | Fabric / Databricks | Either | Spark slightly better |
| > 10 GB | Fabric / Databricks | Spark | Distributed processing |

See **spark-pandas-best-practices** skill for optimization details.

---

## Configuration Management

Never hardcode values:

```python
# BAD
TABLE_NAME = "prod_orders_daily"
BATCH_SIZE = 5000

# GOOD
import os
TABLE_NAME = os.getenv("TABLE_NAME", "dev_orders_daily")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "5000"))

# In production, set env vars
# export TABLE_NAME="prod_orders_daily"
```

---

## Logging Pattern

```python
import logging

logger = logging.getLogger(__name__)

# Informational
logger.info(f"Loaded {N} records from {source}")

# Warnings (recoverable)
logger.warning(f"Skipped {skipped} invalid rows")

# Errors (pipeline impact)
logger.error(f"Transform failed: {error}")

# Debug (for troubleshooting)
logger.debug(f"Batch {batch_id}: {row_count} rows processed")
```

---

## Common Data Issues & Fixes

| Issue | Symptom | Fix |
|-------|---------|-----|
| Silent nulls | Rows silently dropped | Explicit `assert` before dropna() |
| Schema drift | Unexpected columns | Define schema in config; validate on load |
| Duplicates | Same record twice | Check `df.duplicated(subset=["id"])` |
| Encoding errors | "UnicodeDecodeError" | Specify encoding: `pd.read_csv(..., encoding='utf-8')` |
| Memory spike | "MemoryError" on large data | Use `dtype` on load, chunk files, or use Spark |

---

## Related Skills

- **spark-pandas-best-practices**: Framework choice & optimization
- **data-quality-testing**: Detailed validation patterns
- **data-pipeline-tdd**: TDD for pipelines
- **capture-data-eng-lessons**: Logging improvements

---

## References

- [Data Validation Best Practices](https://greatexpectations.io/gx-core)
- [Pandas I/O Tools](https://pandas.pydata.org/docs/user_guide/io.html)
- [Spark Tuning Guide](https://spark.apache.org/docs/latest/tuning.html)
