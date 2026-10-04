import logging
from pathlib import Path

from src.database.connection import get_connection

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CREATE_SCHEMA_SQL = (
    PROJECT_ROOT
    / "src"
    / "database"
    / "sql"
    / "create_core_schema.sql"
)

TRANSFORM_SQL = (
    PROJECT_ROOT
    / "src"
    / "database"
    / "sql"
    / "transform_raw_to_core.sql"
)


def execute_sql_file(file_path: Path) -> None:
    """Execute a SQL file against PostgreSQL."""

    logger.info("Executing %s", file_path.name)

    sql_script = file_path.read_text(encoding="utf-8")

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql_script)

        connection.commit()

    logger.info("Completed %s", file_path.name)


def build_core_layer() -> None:
    """Rebuild the typed relational core layer."""

    execute_sql_file(CREATE_SCHEMA_SQL)
    execute_sql_file(TRANSFORM_SQL)

    logger.info("Core layer built successfully.")


if __name__ == "__main__":
    build_core_layer()