---
name: auto-doc-sync
description: >-
  Keep code and documentation in sync. Detect documentation drift, propose updates
  when code changes, maintain accurate examples, and automate documentation generation
  from docstrings and type hints.
---

# Auto-Doc Sync

## When to Use

- **After code changes**: Function signature changed? Update docs immediately
- **Broken examples**: Code examples in README no longer work?
- **Doc audits**: Is documentation accurate and current?
- **Automated generation**: Generate docs from docstrings/type hints
- **Drift detection**: Find mismatches between code and documentation

---

## Core Principle: Docs Derive from Code

```
Source of Truth: Docstring + Type Hints
        ↓
Actual Documentation: README, API docs (derive from source)
        ↓
Examples: Keep working & tested
```

**Rule**: If code and docs disagree, **code wins**. Update docs immediately.

---

## Step 1: Document with Docstrings & Type Hints

**BAD**: No documentation

```python
def load_data(path):
    return pd.read_csv(path)
```

**GOOD**: Full docstring + type hints

```python
def load_data(path: str, schema: dict = None) -> pd.DataFrame:
    """
    Load CSV data and optionally validate schema.
    
    Args:
        path: Path to CSV file
        schema: Optional column → dtype mapping for validation
    
    Returns:
        pd.DataFrame: Loaded and validated data
    
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If schema validation fails
    
    Example:
        >>> df = load_data("sales.csv", {"id": "int", "amount": "float"})
        >>> df.shape
        (10000, 2)
    """
    df = pd.read_csv(path)
    if schema:
        # Validate schema
        for col, dtype in schema.items():
            if col not in df.columns:
                raise ValueError(f"Column {col} not found")
            df[col] = df[col].astype(dtype)
    return df
```

---

## Step 2: Check for Drift

### What to Check

1. **Function signature changed?**
   - Old: `load_data(file)`
   - New: `load_data(file, schema=None, strict=True)`
   - Find docs that reference old signature → **Update**

2. **Return type changed?**
   - Old: Returns `dict`
   - New: Returns `pd.DataFrame`
   - Find examples showing dict access → **Update**

3. **Examples still work?**
   - Does code example in README run without errors?
   - Does output match the documented output?

4. **Parameters documented?**
   - Does README mention all parameters?
   - Are defaults accurate?

### Drift Detection Workflow

```
1. Scan docstring for current signature
2. Scan README for function references
3. Compare: signature in README matches docstring?
4. Compare: examples in README run with current code?
5. Report mismatches
```

---

## Step 3: Update Documentation

### When Signature Changes

**Old README**:
```markdown
## Usage

Load data:

\`\`\`python
df = load_data("data/sales.csv")
\`\`\`
```

**New signature**: `load_data(path, schema=None, strict=True)`

**Updated README**:
```markdown
## Usage

Load and validate data:

\`\`\`python
df = load_data(
    "data/sales.csv",
    schema={"id": "int", "amount": "float"},
    strict=True
)
\`\`\`
```

### When Behavior Changes

**Old docstring**: "Returns dict with keys: id, amount, date"

**New code**: Returns pd.DataFrame

**Updated docstring**:
```python
def load_data(path):
    """
    Load data from CSV.
    
    Returns:
        pd.DataFrame: With columns [id, amount, date]
    """
```

---

## Step 4: Maintain Examples

**Rule**: Every code example in docs must be **runnable and accurate**.

### Example Template

```markdown
## Example: Load and Process Sales Data

\`\`\`python
# Load data
df = load_data(
    "sales.csv",
    schema={"id": "int", "amount": "float"}
)

# Filter to recent sales
df_recent = df[df["date"] > "2026-01-01"]

# Check shape
print(df_recent.shape)
# Output: (8500, 3)  ← Must match actual output!
\`\`\`
```

### Verify Examples Work

```bash
# Use pytest to validate examples in docstrings
pytest --doctest-modules src/data/pipelines.py

# Run examples from README (manual or with tools like nbval)
```

---

## Automation Opportunities

### Auto-Generate Docs from Type Hints

```python
# src/data/pipelines.py
def transform(
    df: pd.DataFrame,
    discount_rate: float = 0.1,
    min_amount: float = 100.0
) -> pd.DataFrame:
    """Apply transformations to sales data."""
    ...

# Can auto-generate:
# transform(df: DataFrame, discount_rate: float = 0.1, min_amount: float = 100.0) -> DataFrame
```

### Auto-Generate from Docstrings

**Sphinx**: Reads docstrings → Generates HTML docs

```bash
sphinx-apidoc -o docs/source src/
make html  # Generates full API docs from docstrings
```

---

## Workflow: After Code Change

### Checklist

1. **Change made** (e.g., added parameter `strict=True`)
2. **Update docstring** (add to Args section)
3. **Update example in docstring** (show new parameter)
4. **Update README** (if referenced)
5. **Test example** (run the code, verify output)
6. **Commit**: `docs: update [function] signature and examples`

### Git Commit Message

```
feat: add strict validation mode to load_data

- New parameter: strict=True (enforce all columns in schema)
- Updated docstring with new parameter
- Updated README example showing strict mode
- Tests passing
```

---

## Anti-Patterns

### ❌ Anti-Pattern 1: Docs Out of Sync

```python
# BAD: Function returns DataFrame, docs say dict
def load_data(path):
    """Returns: dict with keys id, amount"""
    return pd.read_csv(path)

# GOOD: Docs match code
def load_data(path):
    """Returns: pd.DataFrame with columns [id, amount, date]"""
    return pd.read_csv(path)
```

### ❌ Anti-Pattern 2: Example Code Doesn't Run

```python
# BAD: README example doesn't work
"""
Load data:

\`\`\`python
df = load_data("file.csv")
print(df.my_missing_column)  # This column doesn't exist!
\`\`\`
"""

# GOOD: Example tested
"""
Load data:

\`\`\`python
df = load_data("file.csv")
print(df.head())  # ✓ Works
\`\`\`
"""
```

### ❌ Anti-Pattern 3: Hidden Assumptions

```python
# BAD: Docs don't explain assumptions
def process_data(df):
    """Process data."""  # What assumptions?
    return df[df["amount"] > 0]

# GOOD: Assumptions documented
def process_data(df):
    """
    Process data.
    
    Assumes:
        - 'amount' column exists
        - Negative amounts should be removed per policy
    """
    return df[df["amount"] > 0]
```

---

## Platforms

### Local Python

```python
# Use NumPy-style docstrings
def my_function(param1: int) -> str:
    """
    Short description.
    
    Long description.
    
    Parameters
    ----------
    param1 : int
        Description of param1
    
    Returns
    -------
    str
        Description of return value
    """
```

### Databricks / Fabric Notebooks

```python
# Docstrings in cells link to overview
def my_function(param1):
    """
    See comprehensive docs at: notebook_root/readme
    """
```

---

## References

- [NumPy Docstring Guide](https://numpydoc.readthedocs.io/en/latest/format.html)
- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Type Hints (PEP 484)](https://www.python.org/dev/peps/pep-0484/)
