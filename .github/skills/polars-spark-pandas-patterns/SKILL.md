---
name: polars-spark-pandas-patterns
description: >-
  Choose the right dataframe engine and apply performant patterns across Polars,
  Spark, and Pandas. Use when deciding execution strategy, reviewing
  vectorization, or migrating code toward the repo's Polars-first defaults.
---

# Polars Spark Pandas Patterns

This repo is Polars-first.

Use:
- Polars by default for local and Python-runtime execution
- Spark when the workload genuinely needs distributed execution
- Pandas mainly for compatibility with existing code or specific libraries

## Decision Rules

- `<10GB local`: prefer Polars
- `Fabric/Databricks Python runtime`: prefer Polars unless a distributed Spark workload is clearly required
- `Large distributed joins or cluster-native workloads`: consider Spark
- `Legacy library pressure`: tolerate Pandas, but avoid new Pandas-first designs unless necessary

## Review Targets

- row-wise operations that should be expressions
- eager loading that should be lazy or pushdown-friendly
- Spark usage where Python runtime plus Polars would be simpler and cheaper
- Pandas patterns that should be migrated or isolated
