---
name: data-quality-testing
description: >-
  Build schema checks, data validators, and pytest-based quality tests for data
  pipelines. Use when adding or hardening validation logic and when you want
  concrete fixture or validator templates to start from.
allowed-tools:
  - read
  - write
  - shell(pytest:*)
---

# Data Quality Testing

Use this skill to turn vague "the data looks wrong" concerns into explicit validators, fixtures, and tests.

## Assets In This Skill

- `examples/validator_pandas.py`: starter validator for Pandas-based outputs
- `examples/validator_polars.py`: starter validator for Polars-based outputs
- `examples/test_quality_pytest.py`: pytest template for pipeline quality checks

## Workflow

1. Define the contract:
   - required columns
   - required types
   - null policy
   - uniqueness policy
   - business-rule constraints
2. Pick the nearest validator example and adapt it.
3. Add a pytest file based on `examples/test_quality_pytest.py`.
4. Run focused tests until the contract is enforceable.
5. Keep the validator close to the transformation it protects.

## Typical Usage

```text
Use data-quality-testing to add explicit validators for order_id uniqueness, non-null keys, and valid status values. Start from the Polars validator example and create pytest coverage.
```

## Principles

- Validate structure before content.
- Prefer explicit assertions over silent cleanup.
- Every recurring bug should become a regression test.
- Small fixtures are better than hidden implicit data state.
