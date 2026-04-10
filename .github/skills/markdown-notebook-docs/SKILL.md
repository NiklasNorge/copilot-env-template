---
name: markdown-notebook-docs
description: >-
  Write clear, well-structured markdown documentation for notebooks and code.
  Create data dictionaries, API docs, architecture diagrams, and guides that explain
  intent and usage.
---

# Markdown Notebook Docs

## When to Use

- **Creating README for a project**: Overview, setup, usage
- **Data dictionaries**: Define columns, types, business meanings
- **API documentation**: Describe endpoints, parameters, responses
- **Architecture guides**: Explain system/pipeline design
- **Runbooks**: Step-by-step operational guides
- **Notebooks**: Add markdown cells to guide readers

---

## Structure: README Template

### For Data Pipelines

```markdown
# Project Name

**Purpose**: One-line description of what this does

**Owner**: Your name  
**Last Updated**: YYYY-MM-DD  
**Status**: Production / Development

---

## Quick Start

\`\`\`bash
make test          # Run tests
make run           # Run pipeline  
make lint          # Check code style
\`\`\`

---

## Overview

What does this pipeline do? What data goes in, what comes out?

### Data Flow

\`\`\`
Source → Load → Transform → Validate → Store → Use
\`\`\`

### Key Metrics

- **Input**: X rows/day from [source]
- **Output**: Y rows/day to [destination]
- **Frequency**: Daily at 2 AM UTC
- **SLA**: Complete within 30 min

---

## Data Dictionary

### Input Schema

| Column | Type | Meaning | Constraints |
|--------|------|---------|------------|
| transaction_id | int | Unique transaction ID | NOT NULL, PRIMARY KEY |
| customer_id | int | Customer ID | NOT NULL, FK to customers |
| amount | float | Transaction amount | > 0 |
| date | date | Transaction date | <= TODAY() |
| status | string | Payment status | IN ['pending', 'completed', 'failed'] |

### Output Schema

[Similar table for output]

---

## Transformations

### Step 1: Load
- Source: [table/file]
- Expected format: [format]

### Step 2: Clean
- Remove nulls in [columns]
- Fix date format issues

### Step 3: Aggregate
- Group by [dimensions]
- Aggregate [measures]

### Step 4: Validate
- Assert [constraints]
- Check [quality rules]

### Step 5: Store
- Destination: [table/file]
- Partition by: [column] for performance

---

## Quality Checks

| Check | Rule | Severity |
|-------|------|----------|
| Schema | Columns match expected | CRITICAL |
| Nulls | No nulls in key columns | CRITICAL |
| Duplicates | No duplicate transaction_ids | MAJOR |
| Range | Amount between 0 and 10000 | MAJOR |
| Freshness | Date within last 7 days | MAJOR |

---

## Usage

### Running Locally

\`\`\`bash
python src/data/pipelines/load_transform_store.py
\`\`\`

### Running on Databricks

\`\`\`python
# Navigate to: /Repos/[user_name]/project-name
%run ./src/data/pipelines/load_transform_store.py
\`\`\`

### Running on Schedule (Databricks Jobs)

[Job configuration or link]

---

## Troubleshooting

### Pipeline Fails with "Schema Mismatch"
- **Cause**: Source format changed
- **Fix**: Update schema in [config file]
- **Prevention**: Source owner should notify us of schema changes

### Memory Error on Large Data Days
- **Cause**: Too many rows for Pandas
- **Fix**: Switch to PySpark, enable partitioning
- **Prevention**: Monitor daily row counts; trigger upgrade if >500K rows

---

## References

- [Data Source Docs](https://link)
- [Architecture Decision](docs/ARCHITECTURE.md)
- [Quality Standards](docs/DATA-PLATFORM-GUIDE.md)
- [Contact](mailto:owner@company.com)
```

---

## Structure: Data Dictionary

```markdown
# Data Dictionary: Sales Dataset

## Table: fact_sales

**Purpose**: Daily sales transactions  
**Owner**: Analytics team  
**Refresh**: Every 2 hours  
**Partitioned by**: date (YYYY-MM-DD)  

### Columns

#### transaction_id (INT)
- **Meaning**: Unique identifier for each transaction
- **Format**: Sequential integer
- **Constraints**: PRIMARY KEY, NOT NULL
- **Example**: 1, 2, 3, ...
- **Business Rules**: Unique per transaction; never reused

#### customer_id (INT)
- **Meaning**: Reference to customer
- **Format**: Integer
- **Constraints**: NOT NULL, FK to dim_customers.id
- **Example**: 12345
- **Business Rules**: Must exist in customer master

#### order_date (DATE)
- **Meaning**: Day transaction occurred
- **Format**: YYYY-MM-DD
- **Constraints**: NOT NULL, <= TODAY()
- **Example**: 2026-04-10
- **Business Rules**: Cannot be future date

#### amount (DECIMAL(10,2))
- **Meaning**: Transaction value in USD
- **Format**: Currency with 2 decimals
- **Constraints**: > 0, NOT NULL
- **Example**: 99.99
- **Business Rules**: Minimum order $0.01; no promotional discounts applied

#### status (VARCHAR(20))
- **Meaning**: Payment processing status
- **Format**: String
- **Constraints**: IN ['pending', 'completed', 'failed', 'refunded']
- **Example**: 'completed'
- **Business Rules**: See status transitions below

### Status Transitions

\`\`\`
pending → completed (normal path)
pending → failed (payment declined)
completed → refunded (customer request)
failed ↛ (terminal state)
\`\`\`

### Quality Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Null rate | 0% | < 0.1% |
| Duplicate rate | 0% | 0% |
| Freshness | < 2 hours | |
| Row count | 1M/day | 0.8-1.2M/day |
```

---

## Structure: API Documentation

```markdown
# ETL Pipeline API

## Endpoints

### POST /load

Load data from source.

**Request**:
\`\`\`json
{
  "source": "s3://bucket/path/data.csv",
  "format": "csv",
  "schema": {"id": "int", "amount": "float"}
}
\`\`\`

**Response** (200):
\`\`\`json
{
  "rows_loaded": 10000,
  "columns": ["id", "amount"],
  "status": "success"
}
\`\`\`

**Response** (400):
\`\`\`json
{
  "error": "Schema mismatch",
  "expected": ["id", "amount"],
  "actual": ["id", "revenue"]
}
\`\`\`

---

### POST /transform

Transform loaded data.

...

---

### POST /validate

Validate transformed data against quality rules.

...
```

---

## Structure: Notebook Markdown Cells

Use markdown cells to guide readers through notebooks:

```markdown
# Data Exploration: Sales Analysis

## Purpose

Analyze sales trends by region and product category for Q1 2026.

## Key Questions

1. Which regions have highest revenue?
2. What's the trend by category?
3. Any anomalies or outliers?

---

## 1. Load and Inspect

Run the cell below to load the dataset.

---

## 2. Data Quality Checks

Verify no nulls, schema matches expected, etc.

---

## 3. Revenue by Region

Aggregate and visualize by region.

---

## 4. Findings & Next Steps

- [Finding 1]
- [Finding 2]ş
- Recommended action: [...]
```

---

## Best Practices

### ✅ DO: Explain WHY

```markdown
# Bad: Explains what
Filter to amounts > $100 to remove small orders.

# Good: Explains why
## Filter to High-Value Orders

Remove orders under $100 per business rule (minimum order policy).
This allows us to focus analysis on customers with meaningful spend.
```

### ✅ DO: Use Examples

```markdown
# Bad: Generic description
Type: Decimal number representing currency

# Good: With examples
Type: Decimal(10, 2) representing USD  
Examples: 99.99, 0.01, 1000000.00

# Invalid values: -50.00 (negatives not allowed), 99.9 (needs 2 decimals)
```

### ✅ DO: Link Related Docs

```markdown
# Link to related

[Data Dictionary](./data-dictionary.md) — Full schema details  
[Quality Standards](./quality.md) — Our validation rules  
[FAQs](./faq.md) — Common questions  
```

---

## Anti-Patterns

### ❌ Documents the WHAT Instead of WHY

```markdown
# BAD
The pipeline removes null values. The status must be active.

# GOOD
The pipeline removes null values because incomplete records bias analysis.
Status filtered to 'active' because historical/archived records add noise.
```

### ❌ Outdated Examples

```markdown
# BAD (Example doesn't work with current code)
Load data:  

\`\`\`bash
pipeline run --source=/old/path/data.csv  # Path no longer exists!
\`\`\`

# GOOD (Examples are current and working)
Load data:

\`\`\`bash
pipeline run --source=s3://bucket/data/2026-04-10/data.csv
\`\`\`
```

### ❌ Orphaned Documentation

```markdown
# BAD: No context
| Column | Type |
| id | int |

# GOOD: Full context
### fact_sales.id

**Meaning**: Unique transaction ID  
**Type**: INT  
**Constraints**: PRIMARY KEY  
**Example**: 123456  
```

---

## Tools

- **Markdown editors**: VS Code, Notepads, GitHub-flavored markdown
- **Diagram tools**: [Mermaid](https://mermaid.js.org/), draw.io
- **Docstring to HTML**: Sphinx, pdoc
- **README templates**: Make a README, README generator

---

## References

- [Diátaxis Documentation Framework](https://diataxis.fr/)
- [Google Technical Writing](https://developers.google.com/tech-writing)
- [Markdown Guide](https://www.markdownguide.org/)
