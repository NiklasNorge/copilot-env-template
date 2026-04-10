import polars as pl

from src.notebooks.sales_helpers import summarize_daily_sales


def test_summarize_daily_sales_returns_one_row_per_date() -> None:
    source = pl.DataFrame(
        {
            "sale_date": ["2026-01-01", "2026-01-01", "2026-01-02"],
            "amount": [10.0, 15.0, 20.0],
        }
    )

    result = summarize_daily_sales(source)

    assert result.height == 2
    assert set(result.columns) == {"sale_date", "total_amount"}
