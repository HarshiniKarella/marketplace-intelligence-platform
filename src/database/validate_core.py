import logging

from psycopg import sql

from src.database.connection import get_connection


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


EXPECTED_COUNTS = {
    "customers": 99_441,
    "orders": 99_441,
    "order_items": 112_650,
    "order_payments": 103_886,
    "order_reviews": 99_224,
    "products": 32_951,
    "sellers": 3_095,
    "product_categories": 73,
}


def get_row_count(table_name: str) -> int:
    """Return the number of rows in a core table."""

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                sql.SQL("SELECT COUNT(*) FROM core.{}").format(
                    sql.Identifier(table_name)
                )
            )

            return cursor.fetchone()[0]


def validate_core_counts() -> None:
    """Validate expected row counts for core tables."""

    validation_failed = False

    for table_name, expected_count in EXPECTED_COUNTS.items():
        actual_count = get_row_count(table_name)

        matches = actual_count == expected_count

        logger.info(
            "%-25s expected=%-10s actual=%-10s match=%s",
            table_name,
            f"{expected_count:,}",
            f"{actual_count:,}",
            matches,
        )

        if not matches:
            validation_failed = True

    if validation_failed:
        raise RuntimeError(
            "Core validation failed: row counts do not match."
        )

    logger.info("All core table row counts validated successfully.")


if __name__ == "__main__":
    validate_core_counts()