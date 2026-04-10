# Databricks Runtime Readiness Checklist

- Is this workload still suitable for Polars-first execution?
- If Spark is used, is there a concrete distributed execution reason?
- Are `dbutils` calls isolated from transform logic?
- Are quality checks explicit for key columns and row-count expectations?
- Is the extracted logic importable and testable outside notebook cells?
