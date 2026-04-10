---
name: data-quality-testing
description: >-
  Validate datasets with schema checks, assertions, and pytest patterns.
  Write quality validators, create test fixtures, and flag data anomalies
  (nulls, duplicates, constraint violations).
---

# Data Quality Testing Skill

## When to Use

- **Validating pipelines**: Schema, cardinality, null/duplicate checks on outputs
- **Writing tests**: Creating pytest fixtures and assertions for data-driven tests
- **Debugging anomalies**: Tracking down unexpected nulls, duplicates, or values
- **Quality rules**: Defining and automating data constraints (e.g., amounts > 0)
- **Fixtures**: Creating minimal reproducible sample data for tests

---

## How to Use

### Step 1: Define Your Constraints

Start by documenting what "good" data looks like:

```python
# BAD: No documented constraints
def validate_output(df):
    pass

# GOOD: Explicit constraints
def validate_output(df):
    """Validate output schema and constraints."""
    # Schema constraint
    assert set(df.columns) == {"id", "amount", "date", "status"}, "Schema mismatch"
    
    # Type constraints
    assert df["id"].dtype == "int64", "id must be int64"
    assert df["amount"].dtype == "float64", "amount must be float64"
    
    # Value constraints
    assert (df["amount"] > 0).all(), "All amounts must be positive"
    assert df["status"].isin(["active", "inactive", "expired"]).all(), "Invalid status"
    
    # Cardinality constraints
    assert df.shape[0] > 0, "DataFrame is empty"
    assert df["id"].duplicated().sum() == 0, "Duplicate IDs found"
    assert df[["id"]].isnull().sum().sum() == 0, "Nulls in key columns"
    
    return True
```

### Step 2: Create Test Fixtures

Small, reproducible datasets for testing:

```python
# tests/fixtures/sample_data.py
import pandas as pd

def sample_valid_data() -> pd.DataFrame:
    """Minimal valid dataset for testing."""
    return pd.DataFrame({
        "id": [1, 2, 3],
        "amount": [10.5, 20.3, 15.0],
        "date": ["2026-01-01", "2026-01-02", "2026-01-03"],
        "status": ["active", "inactive", "active"],
    })

def sample_edge_case_data() -> pd.DataFrame:
    """Edge cases: boundary values, zero amounts."""
    return pd.DataFrame({
        "id": [1, 2],
        "amount": [0.01, 999999.99],  # Min and max realistic values
        "date": ["2026-01-01", "2026-12-31"],
        "status": ["active", "expired"],
    })
```

### Step 3: Write Tests

Use pytest with fixtures to validate transformations:

```python
# tests/test_transformations.py
import pytest
from src.data.pipelines import transform
from tests.fixtures.sample_data import sample_valid_data, sample_edge_case_data
from src.data.validators import validate_output

class TestTransform:
    def test_transform_valid_input(self):
        """Test transform with valid data."""
        df_input = sample_valid_data()
        df_output = transform(df_input)
        
        assert df_output.shape[0] > 0
        assert validate_output(df_output)
    
    def test_transform_preserves_rows(self):
        """Test transform doesn't drop rows without reason."""
        df_input = sample_valid_data()
        df_output = transform(df_input)
        
        # Assuming no rows should be dropped
        assert df_output.shape[0] == df_input.shape[0]
    
    def test_transform_edge_cases(self):
        """Test transform handles boundary values."""
        df_input = sample_edge_case_data()
        df_output = transform(df_input)
        
        assert validate_output(df_output)
    
    def test_transform_null_handling(self):
        """Test transform behavior with nulls."""
        df_input = sample_valid_data().copy()
        df_input.loc[0, "amount"] = None
        df_output = transform(df_input)
        
        # Either drop nulls or raise error; never silent-fail
        if len(df_output) < len(df_input):
            logger.warning("Null rows dropped during transform")
        else:
            raise ValueError("Transform should handle nulls explicitly")
```

### Step 4: Validate in Pipeline

Call validators in your pipeline:

```python
# src/data/pipelines/load_transform_store.py
def main():
    logger.info("Loading...")
    df = load(CONFIG["source"])
    
    logger.info("Transforming...")
    df = transform(df)
    
    logger.info("Validating...")
    assert validate_output(df), "Validation failed"
    
    logger.info("Storing...")
    store(df, CONFIG["destination"])
    logger.info("Pipeline complete!")
```

---

## Examples

### Pandas Example: Sales Data Validation

```python
def validate_sales_data(df):
    """Validate daily sales transactions."""
    # Schema
    expected_cols = {"transaction_id", "customer_id", "amount", "date", "status"}
    assert set(df.columns) == expected_cols, f"Missing columns: {expected_cols - set(df.columns)}"
    
    # Types
    assert df["transaction_id"].dtype == "int64"
    assert df["amount"].dtype == "float64"
    
    # Business rules
    assert (df["amount"] > 0).all(), "Negative amounts found"
    assert df["status"].isin(["pending", "completed", "failed"]).all()
    assert (df["date"] <= pd.Timestamp.now()).all(), "Future dates found"
    
    # Uniqueness
    assert df["transaction_id"].duplicated().sum() == 0, "Duplicate transaction IDs"
    
    # Cardinality
    assert df.shape[0] > 0, "No data"
    assert df.isnull().sum().sum() == 0, "Nulls found"
    
    logger.info(f"✓ Validated {df.shape[0]} transactions")
    return True
```

### PySpark Example: Partition Validation

```python
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, when, count

def validate_spark_daily_data(df: DataFrame, expected_date: str) -> bool:
    """Validate Spark DataFrame for daily ETL."""
    # Schema
    required_cols = ["id", "value", "load_date"]
    assert all(col in df.columns for col in required_cols)
    
    # Partition check
    df_filtered = df.filter(col("load_date") == expected_date)
    row_count = df_filtered.count()
    assert row_count > 0, f"No data for {expected_date}"
    
    # Quality checks
    null_counts = df_filtered.select(
        [count(when(col(c).isNull(), 1)).alias(c) for c in required_cols]
    ).collect()[0].asDict()
    
    assert all(v == 0 for v in null_counts.values()), f"Nulls found: {null_counts}"
    
    logger.info(f"✓ Validated {row_count} rows for {expected_date}")
    return True
```

---

## Anti-Patterns

### ❌ Anti-Pattern 1: Silent Failures

```python
# BAD: Silently drops nulls
def transform(df):
    return df.dropna()

# GOOD: Explicit about nulls
def transform(df):
    null_count = df.isnull().sum().sum()
    if null_count > 0:
        logger.warning(f"Dropping {null_count} null values")
    return df.dropna()
```

### ❌ Anti-Pattern 2: No Context on Failures

```python
# BAD: Generic assertion
assert df.shape[0] > 0

# GOOD: Informative assertion
rows_loaded = df.shape[0]
assert rows_loaded > 0, f"No data loaded from {source}; check if source is available"
```

### ❌ Anti-Pattern 3: Missing Fixture Data

```python
# BAD: Test assumes implicit data state
def test_transform():
    df = transform(get_data())  # What is get_data()?
    assert len(df) > 0

# GOOD: Explicit fixture
def test_transform(sample_data_fixture):
    df = transform(sample_data_fixture)
    assert len(df) > 0
```

---

## Patterns by Framework

### pytest + Pandas

```python
@pytest.fixture
def sample_df():
    return pd.DataFrame({...})

def test_with_fixture(sample_df):
    result = transform(sample_df)
    assert isinstance(result, pd.DataFrame)
    assert result.shape[0] > 0
```

### pytest + PySpark

```python
@pytest.fixture(scope="session")
def spark_session():
    return SparkSession.builder.master("local[*]").appName("test").getOrCreate()

def test_spark_transform(spark_session):
    df = spark_session.createDataFrame([...], schema="...")
    result = transform(df)
    assert result.count() > 0
```

---

## References

- [pytest docs](https://docs.pytest.org/) — Fixtures, assertions, best practices
- [great_expectations](https://greatexpectations.io/) — Data validation framework (advanced)
- [pandas testing](https://pandas.pydata.org/docs/reference/testing.html) — pd.testing utilities
- [Spark testing](https://spark.apache.org/docs/latest/testing.html) — Spark test patterns
