from pathlib import Path

import pandas as pd
import pytest

from src.ingestion.raw_data_loader import validate_raw_files


def test_validate_raw_files_returns_all_expected_files(tmp_path: Path) -> None:
    expected_files = [
        "olist_customers_dataset.csv",
        "olist_geolocation_dataset.csv",
        "olist_order_items_dataset.csv",
        "olist_order_payments_dataset.csv",
        "olist_order_reviews_dataset.csv",
        "olist_orders_dataset.csv",
        "olist_products_dataset.csv",
        "olist_sellers_dataset.csv",
        "product_category_name_translation.csv",
    ]

    for filename in expected_files:
        pd.DataFrame({"example": [1]}).to_csv(tmp_path / filename, index=False)

    result = validate_raw_files(tmp_path)

    assert len(result) == 9
    assert all(path.exists() for path in result)


def test_validate_raw_files_raises_error_when_file_missing(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        validate_raw_files(tmp_path)