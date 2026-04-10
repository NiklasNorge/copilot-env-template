---
name: data-pipeline-tdd
description: >-
  Test-driven development for data pipelines. Write tests BEFORE code (RED-GREEN-REFACTOR).
  Ensure transformations are correct before deploying.
---

# Data Pipeline TDD

## When to Use

- **Building new pipelines**: Write test first, code to pass test
- **Refactoring**: Ensure behavior stays the same
- **Bug fixes**: Write failing test that reproduces bug, then fix
- **Team confidence**: Tests document expected behavior

---

## The RED-GREEN-REFACTOR Cycle

### RED: Write Failing Test

Start by defining what SUCCESS looks like:

```python
# tests/test_transform.py
import pytest
from src.data.transforms import calculate_discount

def test_calculate_discount_10_percent():
    """Test that discount of 10% is applied correctly."""
    amount = 100.0
    expected = 90.0
    
    result = calculate_discount(amount, rate=0.1)
    
    assert result == expected
```

**Run test** → ❌ FAILS (function doesn't exist yet)

### GREEN: Write Minimal Code to Pass

```python
# src/data/transforms.py
def calculate_discount(amount: float, rate: float = 0.1) -> float:
    """Apply discount to amount."""
    return amount * (1 - rate)
```

**Run test** → ✅ PASSES

### REFACTOR: Improve Without Breaking

```python
# src/data/transforms.py
def calculate_discount(amount: float, rate: float = 0.1) -> float:
    """
    Apply discount to amount.
    
    Args:
        amount: Original amount
        rate: Discount as decimal (0.1 = 10%)
    
    Returns:
        Discounted amount
    """
    discount_factor = 1 - rate
    return amount * discount_factor
```

**Run test** → ✅ PASSES (behavior unchanged)

---

## Step 1: Write Tests for All Cases

### Happy Path

```python
def test_filter_active_orders():
    """Test that filter returns only active orders."""
    df_input = pd.DataFrame({
        "order_id": [1, 2, 3, 4],
        "status": ["active", "inactive", "active", "expired"]
    })
    
    result = filter_active_orders(df_input)
    
    assert result.shape[0] == 2
    assert result["status"].unique() == ["active"]
```

### Edge Cases

```python
def test_filter_active_orders_empty_input():
    """Test with empty DataFrame."""
    df_empty = pd.DataFrame({"order_id": [], "status": []})
    
    result = filter_active_orders(df_empty)
    
    assert result.shape[0] == 0

def test_filter_active_orders_no_active_orders():
    """Test when no active orders exist."""
    df_inactive = pd.DataFrame({
        "order_id": [1, 2],
        "status": ["inactive", "expired"]
    })
    
    result = filter_active_orders(df_inactive)
    
    assert result.shape[0] == 0
```

### Error Cases

```python
def test_filter_active_orders_missing_column():
    """Test with missing status column."""
    df_bad = pd.DataFrame({"order_id": [1, 2]})
    
    with pytest.raises(KeyError):
        filter_active_orders(df_bad)
```

---

## Step 2: Use Fixtures for Reusable Test Data

```python
# tests/conftest.py
@pytest.fixture
def sample_orders():
    """Standard test dataset."""
    return pd.DataFrame({
        "order_id": [1, 2, 3, 4, 5],
        "customer_id": [10, 10, 20, 20, 30],
        "amount": [100, 200, 150, 300, 50],
        "status": ["active", "inactive", "active", "completed", "cancelled"],
        "date": ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04", "2026-01-05"]
    })

@pytest.fixture
def sample_orders_with_nulls():
    """Dataset with nulls for edge case testing."""
    df = sample_orders()
    df.loc[0, "amount"] = None
    df.loc[2, "status"] = None
    return df

# Use in tests
def test_transform_keeps_nulls(sample_orders_with_nulls):
    result = transform(sample_orders_with_nulls)
    assert result.isnull().sum().sum() > 0
```

---

## Step 3: Build Test Suite for Entire Pipeline

```python
# tests/test_pipeline.py
class TestEtlPipeline:
    """Test full ETL pipeline."""
    
    def test_load_valid_file(self):
        """Test loading valid CSV."""
        df = load_data("tests/fixtures/sample.csv")
        assert df.shape[0] > 0
    
    def test_load_missing_file(self):
        """Test loading non-existent file."""
        with pytest.raises(FileNotFoundError):
            load_data("non_existent.csv")
    
    def test_transform_basic(self, sample_orders):
        """Test transform logic."""
        result = transform(sample_orders)
        assert result.shape[0] > 0
        assert "discount" in result.columns
    
    def test_validate_passes(self, sample_orders):
        """Test validation on clean data."""
        assert validate_and_store(sample_orders) is True
    
    def test_validate_fails_on_nulls(self, sample_orders_with_nulls):
        """Test validation rejects data with nulls."""
        with pytest.raises(AssertionError):
            validate_and_store(sample_orders_with_nulls)
    
    def test_end_to_end(self):
        """Test complete pipeline: load → transform → validate → store."""
        main()  # Runs entire pipeline
        
        # Check output file was created
        assert os.path.exists("output/processed.csv")
        
        # Check output is valid
        df_output = pd.read_csv("output/processed.csv")
        assert df_output.shape[0] > 0
```

---

## Step 4: Run Tests Continuously

```bash
# Run once
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run in watch mode (auto-run on file change)
pytest-watch tests/

# Run specific test
pytest tests/test_transform.py::test_calculate_discount_10_percent
```

---

## Pattern: Testing Data Transformations

### Test Input → Output Contract

```python
def test_aggregate_by_date(sample_orders):
    """Test aggregation maintains data integrity."""
    result = aggregate_by_date(sample_orders)
    
    # Contract: 1 row per unique date
    assert result.shape[0] == sample_orders["date"].nunique()
    
    # Contract: Summed amounts match
    expected_total = sample_orders["amount"].sum()
    actual_total = result["total_amount"].sum()
    assert actual_total == expected_total
```

### Test Idempotence

```python
def test_transform_is_idempotent(sample_orders):
    """Test that transform applied twice = applied once."""
    result_once = transform(sample_orders)
    result_twice = transform(transform(sample_orders))
    
    pd.testing.assert_frame_equal(result_once, result_twice)
```

---

## Anti-Patterns

### ❌ Testing Without Fixtures

```python
# BAD: Recreates data in every test
def test_filter_1():
    df = pd.DataFrame({"id": [1, 2], "status": ["active", "inactive"]})
    assert filter_active(df).shape[0] == 1

def test_filter_2():
    df = pd.DataFrame({"id": [1, 2], "status": ["active", "inactive"]})  # Repeated!
    assert filter_active(df).shape[0] == 1

# GOOD: Use fixture
@pytest.fixture
def sample():
    return pd.DataFrame({...})

def test_filter_1(sample):
    assert filter_active(sample).shape[0] == 1

def test_filter_2(sample):
    assert filter_active(sample).shape[0] == 1
```

### ❌ Testing Implementation Instead of Behavior

```python
# BAD: Tests exact column order (brittle)
def test_transform():
    result = transform(df)
    assert result.columns[0] == "id"  # What if we reorder?

# GOOD: Tests what matters
def test_transform():
    result = transform(df)
    assert "id" in result.columns
    assert result.shape[0] > 0
```

---

## References

- [pytest Documentation](https://docs.pytest.org/)
- [Test-Driven Development](https://en.wikipedia.org/wiki/Test-driven_development)
- [pandas Testing](https://pandas.pydata.org/docs/reference/testing.html)
