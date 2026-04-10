"""Shared pytest fixtures for all tests."""

import os
import pytest
import pandas as pd
import polars as pl
import numpy as np
from pathlib import Path

# ============================================================================
# PANDAS FIXTURES (for compatibility with existing code)
# ============================================================================

@pytest.fixture
def sample_orders():
    """Standard orders dataset for testing (Pandas)."""
    return pd.DataFrame({
        "order_id": [1, 2, 3, 4, 5],
        "customer_id": [10, 10, 20, 20, 30],
        "amount": [100.0, 200.0, 150.0, 300.0, 50.0],
        "status": ["active", "inactive", "active", "completed", "cancelled"],
        "date": ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04", "2026-01-05"]
    })


@pytest.fixture
def sample_orders_with_nulls(sample_orders):
    """Orders dataset with null values for edge case testing (Pandas)."""
    df = sample_orders.copy()
    df.loc[0, "amount"] = None
    df.loc[2, "status"] = None
    return df


@pytest.fixture
def sample_orders_empty():
    """Empty orders dataset (same schema, no rows - Pandas)."""
    return pd.DataFrame({
        "order_id": [],
        "customer_id": [],
        "amount": [],
        "status": [],
        "date": []
    })


@pytest.fixture
def sample_products():
    """Product catalog for join tests (Pandas)."""
    return pd.DataFrame({
        "product_id": [101, 102, 103, 104],
        "product_name": ["Widget A", "Widget B", "Gadget X", "Gadget Y"],
        "category": ["widget", "widget", "gadget", "gadget"],
        "price": [25.0, 35.0, 50.0, 75.0]
    })


# ============================================================================
# POLARS FIXTURES (primary data processing library)
# ============================================================================

@pytest.fixture
def sample_orders_polars():
    """Standard orders dataset for testing (Polars - PRIMARY)."""
    return pl.DataFrame({
        "order_id": [1, 2, 3, 4, 5],
        "customer_id": [10, 10, 20, 20, 30],
        "amount": [100.0, 200.0, 150.0, 300.0, 50.0],
        "status": ["active", "inactive", "active", "completed", "cancelled"],
        "date": ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04", "2026-01-05"]
    })


@pytest.fixture
def sample_orders_polars_with_nulls():
    """Orders dataset with null values for edge case testing (Polars)."""
    return pl.DataFrame({
        "order_id": [1, 2, 3, 4, 5],
        "customer_id": [10, 10, 20, 20, 30],
        "amount": [None, 200.0, 150.0, 300.0, 50.0],
        "status": ["active", "inactive", None, "completed", "cancelled"],
        "date": ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04", "2026-01-05"]
    })


@pytest.fixture
def sample_orders_polars_empty():
    """Empty orders dataset (same schema, no rows - Polars)."""
    return pl.DataFrame({
        "order_id": pl.Series([], dtype=pl.Int64),
        "customer_id": pl.Series([], dtype=pl.Int64),
        "amount": pl.Series([], dtype=pl.Float64),
        "status": pl.Series([], dtype=pl.Utf8),
        "date": pl.Series([], dtype=pl.Utf8)
    })


@pytest.fixture
def sample_products_polars():
    """Product catalog for join tests (Polars)."""
    return pl.DataFrame({
        "product_id": [101, 102, 103, 104],
        "product_name": ["Widget A", "Widget B", "Gadget X", "Gadget Y"],
        "category": ["widget", "widget", "gadget", "gadget"],
        "price": [25.0, 35.0, 50.0, 75.0]
    })


# ============================================================================
# TEMPORARY FILES & DIRECTORIES
# ============================================================================

@pytest.fixture
def tmp_data_dir(tmp_path):
    """Temporary directory for test data files."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return data_dir


@pytest.fixture
def sample_csv_file(tmp_data_dir, sample_orders):
    """Write sample data to CSV file."""
    csv_path = tmp_data_dir / "orders.csv"
    sample_orders.to_csv(csv_path, index=False)
    return csv_path


@pytest.fixture
def sample_parquet_file(tmp_data_dir, sample_orders):
    """Write sample data to Parquet file."""
    parquet_path = tmp_data_dir / "orders.parquet"
    sample_orders.to_parquet(parquet_path, index=False)
    return parquet_path


# ============================================================================
# ENVIRONMENT & CONFIGURATION
# ============================================================================

@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch, tmp_path):
    """Set up test environment variables."""
    monkeypatch.setenv("ENV", "test")
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    yield
    # Cleanup handled by pytest


@pytest.fixture
def mock_config():
    """Mock configuration object."""
    return {
        "batch_size": 1000,
        "min_rows": 100,
        "date_format": "%Y-%m-%d",
        "encoding": "utf-8",
        "db_host": "localhost",
        "db_name": "test_db"
    }


# ============================================================================
# LOGGING
# ============================================================================

@pytest.fixture
def caplog_debug(caplog):
    """Capture logs at DEBUG level."""
    caplog.set_level("DEBUG")
    return caplog


# ============================================================================
# MARKERS
# ============================================================================

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


# ============================================================================
# HOOKS
# ============================================================================

def pytest_collection_modifyitems(config, items):
    """Auto-mark tests based on location."""
    for item in items:
        # Mark tests in tests/integration/ as integration tests
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        # Mark tests in tests/unit/ as unit tests
        elif "unit" in item.nodeid:
            item.add_marker(pytest.mark.unit)
