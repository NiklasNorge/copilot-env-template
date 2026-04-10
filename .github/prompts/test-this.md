---
name: /test-this
description: Generate test cases for a function, class, or module
---

# Test This

**What it does**: Analyzes code and generates comprehensive test cases covering happy path, edge cases, and error scenarios. Creates pytest-ready code with fixtures.

**When to use**:
- Adding test coverage to existing code
- Need to test new function
- TDD: write tests before code

**Example usage**:

```
/test-this

src/data/transforms.py::calculate_discount
```

**Output you'll get**:
- Happy path test cases (normal inputs)
- Edge case tests (empty data, nulls, boundaries)
- Error cases (invalid input, type errors)
- Fixture setup code (reusable test data)
- Full pytest code block
- Copy-paste ready into tests/

**This delegates to**: @CodeReviewer (test quality)
