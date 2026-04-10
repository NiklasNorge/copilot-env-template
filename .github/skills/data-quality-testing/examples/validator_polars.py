import polars as pl


def validate_orders_polars(df: pl.DataFrame) -> None:
    required_columns = {"order_id", "customer_id", "amount", "status"}
    missing = required_columns - set(df.columns)
    assert not missing, f"Missing columns: {sorted(missing)}"

    assert df.select(pl.col("order_id").is_null().sum()).item() == 0, "order_id must be non-null"
    assert df.select(pl.col("order_id").n_unique()).item() == df.height, "order_id must be unique"
    assert df.select((pl.col("amount") <= 0).sum()).item() == 0, "amount must be positive"
    assert df.select(
        pl.col("status").is_in(["active", "inactive", "cancelled"]).all()
    ).item(), "invalid status value"
