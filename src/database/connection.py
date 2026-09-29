import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / ".env"

load_dotenv(ENV_PATH)


def validate_database_config() -> None:
    """Validate that all required database environment variables exist."""

    required_variables = [
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD",
    ]

    missing_variables = [
        variable
        for variable in required_variables
        if not os.getenv(variable)
    ]

    if missing_variables:
        raise RuntimeError(
            f"Missing required database configuration: {missing_variables}"
        )


def get_connection() -> psycopg.Connection:
    """Create and return a direct PostgreSQL connection."""

    validate_database_config()

    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


def get_engine() -> Engine:
    """Create and return a SQLAlchemy PostgreSQL engine."""

    validate_database_config()

    database_url = (
        f"postgresql+psycopg://{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:"
        f"{os.getenv('DB_PORT')}/"
        f"{os.getenv('DB_NAME')}"
    )

    return create_engine(database_url)


if __name__ == "__main__":
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT current_database(), current_user;"
            )

            database_name, user_name = cursor.fetchone()

            print(f"Connected to database: {database_name}")
            print(f"Connected as user: {user_name}")