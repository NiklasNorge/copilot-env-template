---
name: code-review-notebooks
description: >-
  Structured code review for Python files and Jupyter notebooks.
  Provides severity-based feedback (Critical, Major, Minor, FYI) on logic,
  performance, standards, and maintainability.
---

# Code Review Notebooks

## When to Use

- **Before pushing**: Self-review your work against standards
- **PR reviews**: Give and receive structured feedback
- **Learning**: Understand best practices through examples
- **Debugging**: Code review often catches hidden bugs

---

## Rev iew Checklist

### Correctness

- [ ] Logic correct? Does it do what it claims?
- [ ] Edge cases handled? (empty data, nulls, boundary values)
- [ ] Assumptions documented?
- [ ] Type errors? (comparing str to int, etc.)
- [ ] Off-by-one errors in loops?

### Dataframe/Spark-Specific

- [ ] Nulls handled? Silent dropna() is dangerous
- [ ] Schema assumptions documented?
- [ ] Partitioning used? (Spark)
- [ ] Unnecessary collects? (Spark)
- [ ] Memory efficient? (Pandas: dtype, chunking)

### Performance

- [ ] Vectorized operations? (no `.apply()` loops on large data)
- [ ] Unnecessary copies?
- [ ] Partition strategy (Spark)?
- [ ] Broadcast for small joins (Spark)?

### Code Quality

- [ ] PEP 8 compliant?
- [ ] Type hints on public functions?
- [ ] Docstrings (NumPy style)?
- [ ] Comments explain WHY, not WHAT?
- [ ] Magic numbers extracted to constants?

### Testing

- [ ] Is code testable? (dependencies injectable?)
- [ ] Edge cases covered?
- [ ] Test data included or fixtures used?

### Maintainability

- [ ] Clear names? (df vs df_clean vs df_with_discount)
- [ ] Single responsibility? (one function = one job)
- [ ] Extractable to module? (if in notebook)
- [ ] Can someone else understand this?

---

## Severity Levels

| Grade | Impact | Examples | Action |
|-------|--------|----------|--------|
| **CRITICAL** | Code fails, data lost, security risk | Uncaught exception, data corruption, hardcoded credentials | Fix before merge |
| **MAJOR** | Performance <10%, hard to maintain | 100x row-by-row loop, no variable names, untestable | Fix in PR |
| **MINOR** | Code works, could be cleaner | Suboptimal but functional, violates style guide | Consider fixing |
| **FYI** | No action, just info | Good pattern spotted, interesting edge case | Note for learning |

---

## Example: Reviewing a Transform Function

```python
def discount_orders(df):
    for i in range(len(df)):
        df.loc[i, 'amount'] = df.loc[i, 'amount'] * 0.9
    return df
```

### Review Feedback

**CRITICAL**:
1. Performance: Row-by-row loops on large DataFrames are 100x slower than vectorized operations
   - Impact: If df has 1M rows, this takes minutes instead of seconds
   - Fix: `df['amount'] = df['amount'] * 0.9`

**MAJOR**:
2. No documentation
   - Missing: docstring explaining discount rate, business rule justification
   - Fix: Add `"""Apply 10% discount to order amounts per holiday policy."""`

**MINOR**:
3. Magic number (0.9)
   - Could be: `DISCOUNT_RATE = 0.9; df['amount'] = df['amount'] * DISCOUNT_RATE`
   - Why: More maintainable (change in one place) + self-documenting

### Refactored Version (After Review)

```python
HOLIDAY_DISCOUNT_RATE = 0.9

def discount_orders(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply holiday discount to order amounts.
    
    Args:
        df: DataFrame with 'amount' column
    
    Returns:
        DataFrame with discounted amounts
    """
    df['amount'] = df['amount'] * HOLIDAY_DISCOUNT_RATE
    return df
```

---

## Anti-Patterns to Flag

### ❌ Silent Data Loss

```python
# BAD: No explanation of why rows disappear
df = df.dropna()

# GOOD: Log what's being dropped
null_count = len(df) - len(df.dropna())
if null_count > 0:
    logger.warning(f"Dropped {null_count} rows with nulls")
df = df.dropna()
```

### ❌ Unreadable Names

```python
# BAD
df = df[df['a'] > 100]
x = df['b'].sum()

# GOOD
df_high_value = df[df['amount'] > MIN_ORDER_VALUE]
total_revenue = df_high_value['revenue'].sum()
```

### ❌ Untestable Code

```python
# BAD: Can't test in isolation (depends on file I/O)
def process_daily():
    df = pd.read_csv("daily_data.csv")  # Hard-wired path
    df = transform(df)
    df.to_csv("output.csv")

# GOOD: Testable, injectable dependencies
def process_data(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    df = transform(df)
    return df

# Test
def test_process_data():
    df_test = pd.DataFrame(...)
    result = process_data(df_test, default_config)
    assert result.shape[0] > 0
```

---

## Review Conversation

```
Reviewer: "I see row-by-row loops here. Is this intentional?"

Author: "I need to format each amount specially"

Reviewer: "Can we vectorize? Pandas has built-in methods:

    # Current (slow)
    for i in range(len(df)):
        df.loc[i, 'formatted'] = f"${df.loc[i, 'amount']:.2f}"
    
    # Better
    df['formatted'] = df['amount'].apply(lambda x: f"${x:.2f}")
    
    # Best (pure vectorized)
    df['formatted'] = '$' + df['amount'].round(2).astype(str)

I'd go with option 3. Test both and see which is faster?"

Author: "Nice! Let me update and retest."

[Author pushes updated code]

Reviewer: "✓ Much better! Performance improved 10x."
```

---

## Self-Review Checklist (Before Pushing)

- [ ] Run tests: `make test`
- [ ] Lint: `make lint` (or `black`, `ruff`)
- [ ] Type check: `make type-check` (or `mypy`)
- [ ] Manually test main happy path
- [ ] Check edge cases (empty data, nulls, boundary values)
- [ ] Docstrings? (methods, classes, tricky logic)
- [ ] Type hints on public functions?
- [ ] Comments explain WHY, not WHAT?
- [ ] Extractable to `.py`? (if in notebook)
- [ ] Tests added for new code?
- [ ] Examples still work?

---

## References

- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Code Review Best Practices](https://google.github.io/eng-practices/review/reviewer/)
- [Pandas Anti-Patterns](https://pandas.pydata.org/docs/user_guide/enhancing.html)
