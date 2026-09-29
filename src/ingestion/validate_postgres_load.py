import logging

from psycopg import sql

from src.database.connection import get_connection
from src.ingestion.raw_data_loader import load_raw_datasets


logger = logging.getLogger(__name__)


def get_expected_row_counts() -> dict[str, int]:
    """Return expected row counts from the source CSV files."""

    datasets = load_raw_datasets()

    expected_counts = {}

    for dataset_name, dataframe in datasets.items():
        table_name = (
            dataset_name
            .removeprefix("olist_")
            .removesuffix("_dataset")
        )

        expected_counts[table_name] = len(dataframe)

    return expected_counts


def get_database_row_count(table_name: str) -> int:
    """Return the number of rows in a raw PostgreSQL table."""

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                sql.SQL("SELECT COUNT(*) FROM raw.{}").format(
                    sql.Identifier(table_name)
                )
            )

            return cursor.fetchone()[0]


def validate_row_counts() -> None:
    """Compare source CSV row counts with PostgreSQL row counts."""

    expected_counts = get_expected_row_counts()

    validation_failed = False

    for table_name, expected_count in expected_counts.items():
        actual_count = get_database_row_count(table_name)

        matches = expected_count == actual_count

        logger.info(
            "%-35s source=%-10s database=%-10s match=%s",
            table_name,
            f"{expected_count:,}",
            f"{actual_count:,}",
            matches,
        )

        if not matches:
            validation_failed = True

    if validation_failed:
        raise RuntimeError(
            "Raw ingestion validation failed: row counts do not match."
        )

    logger.info("All raw table row counts validated successfully.")


if __name__ == "__main__":
    validate_row_counts()