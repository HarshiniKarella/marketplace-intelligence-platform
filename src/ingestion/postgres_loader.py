import csv
import logging
from pathlib import Path

from psycopg import sql

from src.database.connection import get_connection
from src.ingestion.raw_data_loader import (
    RAW_DATA_DIR,
    validate_raw_files,
)


logger = logging.getLogger(__name__)


def get_table_name(file_path: Path) -> str:
    """Convert an Olist CSV filename into a PostgreSQL table name."""

    return (
        file_path.stem
        .removeprefix("olist_")
        .removesuffix("_dataset")
    )


def load_csv_with_copy(
    file_path: Path,
    table_name: str,
) -> None:
    """Load one CSV file into the PostgreSQL raw schema using COPY."""

    logger.info(
        "Loading %s into raw.%s",
        file_path.name,
        table_name,
    )

    # Parse the CSV header correctly.
    with file_path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as csv_file:
        reader = csv.reader(csv_file)
        columns = next(reader)

    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute(
                sql.SQL("DROP TABLE IF EXISTS raw.{}").format(
                    sql.Identifier(table_name)
                )
            )

            column_definitions = sql.SQL(", ").join(
                sql.SQL("{} TEXT").format(
                    sql.Identifier(column)
                )
                for column in columns
            )

            cursor.execute(
                sql.SQL(
                    "CREATE TABLE raw.{} ({})"
                ).format(
                    sql.Identifier(table_name),
                    column_definitions,
                )
            )

            copy_statement = sql.SQL(
                "COPY raw.{} ({}) "
                "FROM STDIN WITH (FORMAT CSV, HEADER TRUE)"
            ).format(
                sql.Identifier(table_name),
                sql.SQL(", ").join(
                    sql.Identifier(column)
                    for column in columns
                ),
            )

            with file_path.open(
                "r",
                encoding="utf-8-sig",
                newline="",
            ) as csv_file:

                with cursor.copy(copy_statement) as copy:
                    while data := csv_file.read(1024 * 1024):
                        copy.write(data)

        connection.commit()

    logger.info(
        "Loaded raw.%s successfully.",
        table_name,
    )


def load_all_raw_datasets(
    raw_data_dir: Path = RAW_DATA_DIR,
) -> None:
    """Validate and bulk-load all Olist CSVs into PostgreSQL."""

    file_paths = validate_raw_files(raw_data_dir)

    for file_path in file_paths:
        table_name = get_table_name(file_path)

        load_csv_with_copy(
            file_path=file_path,
            table_name=table_name,
        )

    logger.info(
        "Successfully loaded %d raw datasets.",
        len(file_paths),
    )


if __name__ == "__main__":
    load_all_raw_datasets()