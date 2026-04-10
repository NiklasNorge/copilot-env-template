# Runtime Readiness Checklist

- Is the workload small enough for Python runtime plus Polars?
- Are secrets and workspace paths isolated from transformation logic?
- Is the pipeline output written in a format friendly to downstream jobs?
- Are validators present for key columns, row counts, and partition dates?
- Is there a clear reason to use Spark, or is it only inertia?
