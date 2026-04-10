---
name: /analyze-data
description: Explore a dataset for insights, anomalies, and visualization suggestions
---

# Analyze Data

**What it does**: Quick dataset exploration that identifies patterns, flags anomalies, and suggests visualizations.

**When to use**: 
- New dataset investigation
- Exploratory data analysis (EDA)
- Understanding data shape/quality before analysis

**Example usage**:

```
/analyze-data

Analyzing file: orders_2026_Q1.csv
```

**Output you'll get**:
- Dataset shape & dtypes
- Missing values summary
- Statistical summary (min, max, mean, std)
- Top values per column
- Anomaly flags (outliers, patterns)
- Suggested visualizations

**This delegates to**: @DataQuality agent (validation), @CodeReviewer (quality concerns)
