---
name: testing-and-quality.instructions
description: Auto-loads when you open test_*.py or *_test.py files
---

# Testing & Quality Standards

## TDD Workflow: RED → GREEN → REFACTOR

### 1. Red: Write Failing Test

```python
# tests/test_discount.py
def test_apply_discount():
    """Test 10% discount calculation."""
    amount = 100.0
    expected = 90.0
    
    result = apply_discount(amount)  # Function doesn't exist yet
    
    assert result == expected
```

**Run**: `pytest tests/test_discount.py` → ❌ FAILS

### 2. Green: Write Minimal Code

```python
# src/transforms.py
def apply_discount(amount: float) -> float:
    return amount * 0.9
```

**Run**: `pytest tests/test_discount.py` → ✅ PASSES

### 3. Refactor: Improve Without Breaking

```python
# src/transforms.py
DISCOUNT_RATE = 0.1

def apply_discount(amount: float, rate: float = DISCOUNT_RATE) -> float:
    """Apply discount to amount.
    
    Args:
        amount: Original amount
        rate: Discount rate (0.1 = 10%)
    
    Returns:
        Discounted amount
    """
    return amount * (1 - rate)
```

**Run**: `pytest tests/test_discount.py` → ✅ PASSES (still)

---

## Test File Structure

```python
# tests/test_transforms.py
"""Tests for data transformation functions."""

import pytest
import pandas as pd
from src.data.transforms import apply_discount, validate_amounts

@pytest.fixture
def sample_orders():
    """Fixture: Standard test data."""
    return pd.DataFrame({
        "order_id": [1, 2, 3],
        "amount": [100.0, 200.0, 150.0]
    })

class TestApplyDiscount:
    """Group discount-related tests."""
    
    def test_basic_discount(self):
        """Happy path: discount applied correctly."""
        result = apply_discount(100.0)
        assert result == 90.0
    
    def test_zero_discount(self):
        """Edge case: rate=0 means no discount."""
        result = apply_discount(100.0, rate=0.0)
        assert result == 100.0
    
    def test_full_discount(self):
        """Edge case: rate=1.0 means no amount."""
        result = apply_discount(100.0, rate=1.0)
        assert result == 0.0

class TestValidateAmounts:
    """Group validation tests."""
    
    def test_valid_amounts(self, sample_orders):
        """Valid data passes."""
        assert validate_amounts(sample_orders) is True
    
    def test_invalid_amounts_negative(self):
        """Negative amounts rejected."""
        df_bad = pd.DataFrame({"amount": [-100.0]})
        with pytest.raises(AssertionError):
            validate_amounts(df_bad)
```

---

## Fixtures for Reusability

### Conftest Pattern

```python
# tests/conftest.py
"""Shared fixtures for all tests."""

import pytest
import pandas as pd

@pytest.fixture
def sample_orders():
    """Standard orders dataset."""
    return pd.DataFrame({
        "order_id": [1, 2, 3, 4, 5],
        "amount": [100.0, 200.0, 150.0, 300.0, 50.0],
        "status": ["active", "inactive", "active", "completed", "cancelled"]
    })

@pytest.fixture
def sample_with_nulls(sample_orders):
    """Orders with null values for edge cases."""
    df = sample_orders.copy()
    df.loc[0, "amount"] = None
    df.loc[2, "status"] = None
    return df

# Use in any test file
def test_transform_handles_nulls(sample_with_nulls):
    result = transform(sample_with_nulls)
    assert result is not None
```

---

## Coverage Requirements

### Minimum Coverage

- **Critical paths**: 100% (core business logic must be tested)
- **Data transforms**: 90%+ (most paths should be covered)
- **Utils/helpers**: 80%+ (nice to have)

### Run Coverage

```bash
# Generate coverage report
pytest --cov=src --cov-report=html tests/

# Check coverage locally
pytest --cov=src --cov-report=term tests/
```

---

## Data Quality Test Checklist

- [ ] Empty DataFrame: `df.shape[0] == 0`
- [ ] Missing columns: Column not in `df.columns`
- [ ] Null values: `df.isnull().sum() > 0`
- [ ] Duplicates: `df.duplicated(subset=[key]).sum() > 0`
- [ ] Type mismatches: `df[col].dtype != expected`
- [ ] Value ranges: `df[col].min()`, `df[col].max()` outside expected
- [ ] String encoding: Non-ASCII characters, encoding errors

---

## Example: Full Test Suite for Pipeline

```python
# tests/test_pipeline.py
"""Tests for daily ETL pipeline."""

import pytest
import pandas as pd
from src.data.pipelines import load_data, transform, validate, store

@pytest.fixture
def sample_raw_data():
    return pd.DataFrame({
        "order_id": [1, 2, 3],
        "amount": [100.0, 200.0, 150.0],
        "date": ["2026-04-09", "2026-04-09", "2026-04-09"]
    })

def test_load_data_returns_dataframe(sample_raw_data):
    """Load should return DataFrame."""
    result = load_data("test_source")
    assert isinstance(result, pd.DataFrame)

def test_transform_adds_discount_column(sample_raw_data):
    """Transform should add discount column."""
    result = transform(sample_raw_data)
    assert "discount" in result.columns

def test_validate_passes_clean_data(sample_raw_data):
    """Validation should pass clean data."""
    assert validate(sample_raw_data) is True

def test_validate_fails_missing_columns():
    """Validation should fail on schema mismatch."""
    df_bad = pd.DataFrame({"wrong_col": [1, 2]})
    with pytest.raises(AssertionError):
        validate(df_bad)

def test_end_to_end(tmp_path):
    """Full pipeline: load → transform → validate → store."""
    # Setup
    input_file = tmp_path / "test_orders.csv"
    
    # Simulate load → transform → validate → store
    df = load_data(str(input_file))
    df = transform(df)
    assert validate(df) is True
    
    output_file = tmp_path / "test_output.parquet"
    store(df, str(output_file))
    
    # Verify
    assert output_file.exists()
    df_output = pd.read_parquet(output_file)
    assert df_output.shape[0] > 0
```

---

## Anti-Patterns

### ❌ Hard-coded Data

```python
# BAD
def test_discount():
    df = pd.DataFrame({"amount": [100, 200, 150]})
    # Data recreated in every test

# GOOD
@pytest.fixture
def orders():
    return pd.DataFrame({"amount": [100, 200, 150]})

def test_discount(orders):
    # Data from fixture, reusable
```

### ❌ Testing Implementation

```python
# BAD: Tests exact column order (brittle)
def test_transform():
    result = transform(df)
    assert result.columns[0] == "discount"  # What if we reorder?

# GOOD: Tests has required columns
def test_transform():
    result = transform(df)
    assert "discount" in result.columns
```

---

## Related Skills

- **data-quality-testing**: Detailed validation patterns
- **data-pipeline-tdd**: RED-GREEN-REFACTOR workflow
- **code-review-notebooks**: Code quality checks

---

## References

- [pytest Documentation](https://docs.pytest.org/)
- [pandas Testing](https://pandas.pydata.org/docs/reference/testing.html)
- [Test-Driven Development](https://en.wikipedia.org/wiki/Test-driven_development)
