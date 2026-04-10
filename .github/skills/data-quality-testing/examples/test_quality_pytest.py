import polars as pl
import pytest

from src.data.validators.orders import validate_orders_polars


@pytest.fixture
def sample_orders() -> pl.DataFrame:
    return pl.DataFrame(
        {
            "order_id": [1, 2, 3],
            "customer_id": [10, 10, 20],
            "amount": [100.0, 200.0, 150.0],
            "status": ["active", "inactive", "active"],
        }
    )


def test_validate_orders_polars_accepts_valid_input(sample_orders: pl.DataFrame) -> None:
    validate_orders_polars(sample_orders)


def test_validate_orders_polars_rejects_duplicate_ids(sample_orders: pl.DataFrame) -> None:
    bad = sample_orders.with_columns(pl.lit(1).alias("order_id"))
    with pytest.raises(AssertionError):
        validate_orders_polars(bad)
