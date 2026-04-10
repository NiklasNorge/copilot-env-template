---
name: notebook-as-code
description: >-
  Structure Jupyter notebooks for clarity and testability. Organize cells logically,
  extract functions to .py modules, maintain reproducibility, and ensure notebooks
  can be parameterized and versioned.
---

# Notebook as Code

## When to Use

- **Organizing large notebooks**: 200+ lines becoming hard to follow
- **Extracting logic**: Removing repeated code to reusable `.py` modules
- **Testing notebooks**: Making notebook logic testable outside the notebook
- **Parameterizing**: Enabling reproducible runs with different inputs
- **Documenting**: Adding clear markdown guidance throughout

---

## Standard Cell Order

Every well-structured notebook follows this pattern:

### Cell 1: Imports
```python
# Imports
import pandas as pd
import numpy as np
from src.data.transforms import clean_data, aggregate_data
from src.utils.config import CONFIG
```

### Cell 2: Configuration
```python
# Configuration
DATA_PATH = CONFIG["input_data"]
OUTPUT_PATH = CONFIG["output_data"]
DEBUG = False  # Set True for verbose logging
```

### Cell 3: Functions (Logic)
```python
# Functions
def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Process and validate data."""
    df_clean = clean_data(df)
    df_agg = aggregate_data(df_clean)
    return df_agg

def validate_output(df: pd.DataFrame) -> bool:
    """Validate output schema and constraints."""
    assert df.shape[0] > 0
    assert "result" in df.columns
    return True
```

### Cell 4: Execution (Load → Transform → Store)
```python
# Execution
print("Loading data...")
df = pd.read_csv(DATA_PATH)

print("Processing...")
df_result = process_data(df)

print("Validating...")
assert validate_output(df_result)

print("Storing...")
df_result.to_parquet(OUTPUT_PATH)
print("✓ Complete!")
```

### Cell 5+: Analysis/Visualization (Optional)
```python
# Analysis & Results
print(f"Shape: {df_result.shape}")
print(f"Columns: {df_result.columns.tolist()}")
display(df_result.head(10))
```

---

## Rules for Each Cell

| Cell Type | Max Lines | Purpose | Should Contain |
|-----------|-----------|---------|-----------------|
| Imports | No limit | Declare all dependencies | `import`, `from` statements only |
| Config | 10-20 | Set parameters | Variable assignments, no logic |
| Functions | 50-100 per function | Reusable logic | Function definitions, helper code |
| Execution | 30-50 | Run the pipeline | Function calls, I/O, results |
| Analysis | No limit | EDA or viz | Exploration, charts, summaries |

---

## How to Use

### Step 1: Assess Your Current Notebook

```
500 lines?
├─ Mostly raw analysis → Keep as-is (Exploratory)
├─ Mix of logic + analysis → Extract logic (Step 2)
└─ All pipeline logic → Refactor to .py (Step 3)
```

### Step 2: Extract to .py Module

**When**: You have repeated code across cells or >100 lines of logic in one cell.

**Example**: Cleaning function repeated in 3 cells

```python
# BAD: In notebook, repeated across cells
# Cell 3
df["amount"] = df["amount"].fillna(0)
df["date"] = pd.to_datetime(df["date"])

# Cell 5
df["amount"] = df["amount"].fillna(0)  # Repeated!
df["date"] = pd.to_datetime(df["date"])

# GOOD: Extract to src/data/transforms.py
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Fill nulls and parse dates."""
    df["amount"] = df["amount"].fillna(0)
    df["date"] = pd.to_datetime(df["date"])
    return df

# In notebook, import and reuse
from src.data.transforms import clean_data
df_clean = clean_data(df)
```

### Step 3: Make Logic Testable

Once extracted to `.py`, add tests:

```python
# tests/test_transforms.py
import pytest
from src.data.transforms import clean_data

def test_clean_data_fills_nulls():
    """Test that nulls are filled with 0."""
    df_input = pd.DataFrame({
        "amount": [10.0, None, 30.0]
    })
    df_output = clean_data(df_input)
    assert df_output["amount"].isnull().sum() == 0
    assert df_output["amount"][1] == 0
```

### Step 4: Parameterize for Reproducibility

Use config objects instead of hardcoded values:

```python
# BAD: Hardcoded paths
df = pd.read_csv("/Users/niklas/data/sales.csv")
df.to_csv("/Users/niklas/output/processed.csv")

# GOOD: Config-driven
# src/utils/config.py
CONFIG = {
    "input_data": os.getenv("DATA_PATH", "data/sales.csv"),
    "output_data": os.getenv("OUTPUT_PATH", "output/processed.csv"),
}

# Notebook
df = pd.read_csv(CONFIG["input_data"])
df.to_parquet(CONFIG["output_data"])

# Run with different config
os.environ["DATA_PATH"] = "data/sales_2026.csv"
```

---

## Migration Path: From Exploratory to Pipeline

### Phase 1: Exploratory Notebook (Raw Analysis)

```
[Imports] → [EDA] → [Ad-hoc transformations] → [Plots]
```

**Characteristics**: 300+ lines, repeated code, hardcoded paths, no tests

### Phase 2: Organized Notebook (Extracted Logic)

```
[Imports] → [Config] → [Functions] → [Execution] → [Analysis]
```

**Characteristics**: Clear structure, functions extracted but still in notebook

### Phase 3: Modular Code (.py Pipeline)

```
[Notebook as Runner] → Imports functions from src/data/
```

**Characteristics**: Logic in `.py`, notebook just orchestrates and visualizes

### Phase 4: Scheduled Job (Automated)

```
[Python script] or [Databricks Job] → Runs daily without notebook
```

**Characteristics**: No notebook; cron or orchestration tool runs it

---

## Platform-Specific Notes

### Databricks Notebooks

```python
# Cell 1: Imports + Databricks-specific
import pandas as pd
from pyspark.sql import functions as F

# Cell 2: Config from secrets
DB_TOKEN = dbutils.secrets.get(scope="data", key="token")
CATALOG = "main"
SCHEMA = "silver"

# Cell 3+: As normal
# dbutils.notebook.run() for orchestration, not for shared code
```

### Fabric Notebooks

```python
# Similar to Databricks
# Use notebookutils for cross-notebook calls
from notebookutils.mssparkutils.notebook import run
run("path/to/notebook", 60, {"param1": "value1"})
```

### Local Jupyter

```python
# Use %load_ext autoreload for development
%load_ext autoreload
%autoreload 2

from src.data.transforms import clean_data  # Auto-reloads on import
```

---

## Anti-Patterns

### ❌ Anti-Pattern 1: Magic Numbers in Cells

```python
# BAD
discount = df["amount"] * 0.9

# GOOD
DISCOUNT_RATE = 0.9
discount = df["amount"] * DISCOUNT_RATE
```

### ❌ Anti-Pattern 2: Cell Dependencies Hidden

```python
# BAD: Cell 5 requires Cell 3 but it's not obvious
# Cell 3 (might not run)
my_df = pd.read_csv("file.csv")

# Cell 5 (uses my_df, fails if Cell 3 hasn't run)
print(my_df.shape)

# GOOD: Dependencies explicit via functions + config
def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)
```

### ❌ Anti-Pattern 3: No Markdown Guidance

```python
# BAD: No explanation
df = df[df["amount"] > 100]

# GOOD: Markdown cell explaining
# ## Filter to High-Value Orders
# Remove orders under $100 (minimum order value per policy)
df = df[df["amount"] > 100]
```

---

## Checklist for Refactoring

- [ ] **Imports at top** (Cell 1)
- [ ] **Config separate** (Cell 2)
- [ ] **Functions before execution** (Cell 3)
- [ ] **Execution cells clear** (Cell 4)
- [ ] **Each function <100 lines**
- [ ] **Functions have docstrings**
- [ ] **Repeated code extracted to `.py`**
- [ ] **Magic numbers → named constants**
- [ ] **Cell order logical** (dependencies clear)
- [ ] **Tests exist for extracted functions**

---

## References

- [Jupyter Best Practices](https://nbformat.readthedocs.io/)
- [Papermill (Parameterized Notebooks)](https://papermill.readthedocs.io/)
- [Databricks Notebook Docs](https://docs.databricks.com/en/notebooks/index.html)
- [Fabric Notebook Docs](https://learn.microsoft.com/en-us/fabric/data-engineering/notebook-source-control)
