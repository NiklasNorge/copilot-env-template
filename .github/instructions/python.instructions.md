---
name: python.instructions
description: Auto-loads when you open any .py file
---

# Python Coding Standards

## Quick Rules

✅ **DO**:
- Type hints on all public functions: `def load_data(path: str) -> pd.DataFrame:`
- Docstrings (NumPy style) on classes, public methods
- PEP 8: Black formatter, max 100 chars/line
- Absolute imports; group stdlib → third-party → local
- Extract logic >50 lines to separate functions

❌ **DON'T**:
- Hardcoded paths, secrets, database credentials
- Magic numbers (use constants: `MIN_ORDER_VALUE = 100`)
- Bare `except:` (always catch specific exceptions)
- Loops on DataFrames > 10k rows (vectorize instead)

---

## File Structure

```python
"""Module docstring: One-line purpose."""

# Standard library
import os
import logging

# Third-party
import pandas as pd
import numpy as np

# Local
from src.utils import config, helpers

logger = logging.getLogger(__name__)

# Constants
MIN_ROWS = 100
BATCH_SIZE = 1000

def public_function(data: pd.DataFrame) -> int:
    """Public function docstring (NumPy style).
    
    Args:
        data: Input DataFrame
    
    Returns:
        Count of processed rows
    """
    count = _private_helper(data)
    logger.info(f"Processed {count} rows")
    return count

def _private_helper(data: pd.DataFrame) -> int:
    """Private functions prefixed with _."""
    return len(data)
```

---

## Data Engineering Specifics

### Assertions First

```python
# Validate shape & schema BEFORE transform
assert df.shape[0] > 0, "DataFrame is empty!"
assert "id" in df.columns, "Missing 'id' column"
assert df["id"].dtype == "int64", "ID must be int64"
```

### Logging Over Printing

```python
import logging

logger = logging.getLogger(__name__)

# Don't: print(f"Loaded {N} rows")
# Do:
logger.info(f"Loaded {N} rows from {source}")
logger.warning(f"Skipped {skipped} invalid rows")
logger.error(f"Transform failed: {error}")
```

### Config Over Hardcoding

```python
# BAD
db_host = "prod-db-1.example.com"
api_key = "sk_12345678"

# GOOD
import os
db_host = os.getenv("DB_HOST", "localhost")
api_key = os.getenv("API_KEY")
assert api_key, "API_KEY env var not set"
```

---

## Related Skills

- **spark-pandas-best-practices**: Optimization for large datasets
- **data-quality-testing**: Validation patterns
- **notebook-as-code**: Extracting logic to `.py` modules

---

## References

- [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- [NumPy Docstring Guide](https://numpydoc.readthedocs.io/en/latest/format.html)
- [Black Formatter](https://github.com/psf/black)
