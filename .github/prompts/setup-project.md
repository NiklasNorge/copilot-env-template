---
name: /setup-project
description: Bootstrap a new data engineering project with folder structure, starter code, tests
---

# Setup Project

**What it does**: Meta-agent that asks discovery questions (data source, transformations, output, quality rules, platform preference) then scaffolds a complete project structure with starter code.

**When to use**:
- Starting a new data pipeline
- Cloning template for new project
- First-time setup

**Example usage**:

```
/setup-project
```

**Output you'll get**:
- Interactive questions:
  - What's the data source? (CSV, database, API, streaming?)
  - What transformations needed? (aggregation, deduplication, enrichment?)
  - Where should output go? (Lakehouse, API, file share?)
  - Quality rules? (No nulls? Duplicate handling?)
  - Platform? (Local Pandas, Databricks, Fabric?)
  
- Generated:
  - Complete folder structure (src/data/pipelines, tests/, docs/, etc.)
  - Starter pipeline code (`load_transform_store.py`)
  - Pytest fixtures and test templates
  - Data quality validators
  - README with setup instructions
  - Customized pyproject.toml and Makefile

**This delegates to**: @ProjectScaffolder agent (discovery + generation)
