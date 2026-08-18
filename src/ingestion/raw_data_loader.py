from pathlib import Path
import logging

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

EXPECTED_FILES = [
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


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


def validate_raw_files(raw_data_dir: Path) -> list[Path]:
    """
    Verify that every required raw dataset file is available.

    Parameters
    ----------
    raw_data_dir:
        Directory containing the raw CSV files.

    Returns
    -------
    list[Path]
        Paths to all expected CSV files.

    Raises
    ------
    FileNotFoundError
        If one or more required files are missing.
    """

    missing_files = [
        filename
        for filename in EXPECTED_FILES
        if not (raw_data_dir / filename).exists()
    ]

    if missing_files:
        raise FileNotFoundError(
            f"Missing required raw data files: {missing_files}"
        )

    logger.info("Validated %d raw data files.", len(EXPECTED_FILES))

    return [raw_data_dir / filename for filename in EXPECTED_FILES]


def load_raw_datasets(raw_data_dir: Path = RAW_DATA_DIR) -> dict[str, pd.DataFrame]:
    """
    Load all raw Olist datasets into pandas DataFrames.

    Parameters
    ----------
    raw_data_dir:
        Directory containing the raw CSV files.

    Returns
    -------
    dict[str, pd.DataFrame]
        Mapping between dataset names and loaded DataFrames.
    """

    file_paths = validate_raw_files(raw_data_dir)

    datasets = {}

    for file_path in file_paths:
        logger.info("Loading %s", file_path.name)

        dataset_name = file_path.stem
        datasets[dataset_name] = pd.read_csv(file_path)

    logger.info("Successfully loaded %d datasets.", len(datasets))

    return datasets


if __name__ == "__main__":
    datasets = load_raw_datasets()

    for dataset_name, dataframe in datasets.items():
        logger.info(
            "%s: %d rows x %d columns",
            dataset_name,
            dataframe.shape[0],
            dataframe.shape[1],
        )