import polars as pl

from src.data.transforms.orders import deduplicate_orders


def test_deduplicate_orders_keeps_latest_record_per_order_id() -> None:
    source = pl.DataFrame(
        {
            "order_id": [1, 1, 2],
            "updated_at": ["2026-01-01T10:00:00", "2026-01-01T12:00:00", "2026-01-02T09:00:00"],
            "amount": [100.0, 125.0, 50.0],
        }
    )

    result = deduplicate_orders(source)

    assert result.height == 2
    assert result.filter(pl.col("order_id") == 1)["amount"].item() == 125.0
