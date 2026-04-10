import pandas as pd


def validate_orders_pandas(df: pd.DataFrame) -> None:
    required_columns = {"order_id", "customer_id", "amount", "status"}
    missing = required_columns - set(df.columns)
    assert not missing, f"Missing columns: {sorted(missing)}"

    assert df["order_id"].isna().sum() == 0, "order_id must be non-null"
    assert df["order_id"].duplicated().sum() == 0, "order_id must be unique"
    assert (df["amount"] > 0).all(), "amount must be positive"
    assert df["status"].isin(["active", "inactive", "cancelled"]).all(), "invalid status value"
