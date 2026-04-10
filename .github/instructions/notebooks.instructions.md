---
name: notebooks.instructions
description: Auto-loads when you open any .ipynb file
---

# Notebook Coding Standards

## Quick Rules

✅ **DO**:
- Cell order: Imports → Config → Functions → Execution → Logging
- Each cell: Single logical unit, max ~50 lines
- Extract repeated logic to `.py` modules, import into notebook
- Markdown cells explain intent (not syntax)
- Use Papermill for parameterized runs

❌ **DON'T**:
- Cell dependencies unclear (if B depends on A, document it)
- 500+ line notebooks (extract functions to `.py`)
- Magic values (use config cells)
- Direct `print()` debugging (use logging)

---

## Cell Organization

### 1️⃣ Imports

```python
# Imports
import pandas as pd
import numpy as np
import logging

from src.data.pipelines import load, transform
from src.utils import config

logger = logging.getLogger(__name__)
```

### 2️⃣ Config

```python
# Configuration
DB_SOURCE = "lakehouse"
BATCH_SIZE = 1000
MIN_ROWS = 100

logger.info("Config loaded: DB_SOURCE={}, BATCH_SIZE={}".format(DB_SOURCE, BATCH_SIZE))
```

### 3️⃣ Functions

```python
def process_daily(date_str: str) -> pd.DataFrame:
    """Load and process daily data.
    
    Args:
        date_str: Date in YYYY-MM-DD format
    
    Returns:
        Processed DataFrame
    """
    df = load(date_str)
    df = transform(df)
    return df
```

### 4️⃣ Execution

```python
# Main execution
df = process_daily("2026-04-09")
logger.info(f"Processed {len(df)} rows")
```

### 5️⃣ Analysis

```python
# Exploratory analysis (notebook-specific)
df.groupby("region")["revenue"].sum().sort_values()
```

---

## Extraction Pattern

### When to Extract?

❌ **Keep in notebook**:
- One-off analysis
- <50 lines
- Never reused

✅ **Extract to `.py`**:
- >100 lines
- Reused 2+ times
- Core business logic
- Unit-testable

### Before (All in Notebook)

```python
# Notebook cell
def calculate_discount(df, rate=0.1):
    df["discount"] = df["amount"] * (1 - rate)
    return df

def validate_discount(df):
    assert df["discount"].min() >= 0
    assert df["discount"].max() <= df["amount"].max()
    return True

result = calculate_discount(df)
validate_discount(result)
```

### After (Extracted to Module)

```python
# src/data/transforms.py
def calculate_discount(df: pd.DataFrame, rate: float = 0.1) -> pd.DataFrame:
    """Apply discount to amounts."""
    df["discount"] = df["amount"] * (1 - rate)
    return df

def validate_discount(df: pd.DataFrame) -> bool:
    """Validate discount calculations."""
    assert df["discount"].min() >= 0
    assert df["discount"].max() <= df["amount"].max()
    return True
```

```python
# Notebook cell: Now clean and focused
from src.data.transforms import calculate_discount, validate_discount

result = calculate_discount(df)
validate_discount(result)
```

---

## Platform-Specific Notes

### Databricks/Fabric Notebook Magic

```python
# Databricks
%run ../setup.py  # Execute setup script
dbutils.notebook.run("../other_notebook", timeout_seconds=300)

# Fabric
from notebookutils import mssparkutils
# (Similar patterns)

# Avoid hardcoding paths — use config
```

---

## Related Skills

- **notebook-as-code**: Detailed extraction patterns
- **data-quality-testing**: Validation in notebooks
- **code-review-notebooks**: Review checklists

---

## References

- [pandas Documentation](https://pandas.pydata.org/)
- [Databricks Notebooks](https://docs.databricks.com/notebooks/index.html)
- [Microsoft Fabric Notebooks](https://learn.microsoft.com/en-us/fabric/data-engineering/how-to-use-notebook)
