import os
import sys
from logging import WARNING, getLogger
from typing import Optional

import typer
from sqlalchemy import create_engine

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import utils.oguri_utils as oguri_utils

EXTERNAL_CONFIG = oguri_utils.read_config(r"config.toml")
ENGINE = oguri_utils.sqlite_connection("master_db", config=EXTERNAL_CONFIG)


def get_tables_to_extract() -> list[str]:
    """Gets a list of table names that need to be extracted.

    Reads the query from the config that selects the relevant tables, executes it
    against the database, and returns the list of table names.

    Args:
        None

    Returns:
        `list[str]`: The list of table names.
    """
    return oguri_utils.read_database(EXTERNAL_CONFIG["relevant_tables"]["query"], ENGINE).to_series().to_list()


def table_to_csv() -> None:
    """Extracts the specified tables from the database to individual CSV files.

    Iterates through the list of tables to extract, logs the table name,
    queries the full table from the database, and writes the contents to a
    CSV file named after the table in the ../data directory.

    Args:
        None

    Returns:
        None
    """
    tables = get_tables_to_extract()
    while len(tables) > 0:
        working_table = tables.pop()
        getLogger("ProcessLogger").log(WARNING, f"Extracting table: {working_table}")
        # Query the table for ALL data and insert into polars df
        working_df = oguri_utils.read_database(f"SELECT * FROM {working_table}", ENGINE)  # noqa: S608
        working_df.write_csv(f"../data/{working_table}.csv")


def load_tables_to_pg(
    username: str,
    password: str,
    server_host: str,
    port: int,
    db: str,
    schema: str | None = None,
) -> None:
    """Loads the extracted tables into a PostgreSQL database.

    Iterates through the list of tables to extract, connects to the
    provided PostgreSQL database, reads each table from the SQLite
    database into a DataFrame, and writes it to the PostgreSQL database,
    replacing any existing table with the same name.

    Args:
        username: PostgreSQL username
        password: PostgreSQL password
        server_host: PostgreSQL server host
        port: PostgreSQL server port
        db: PostgreSQL database name
        schema: Optional PostgreSQL schema name to write tables into

    Returns:
        None
    """
    tables = get_tables_to_extract()
    pg_engine = create_engine(f"postgresql://{username}:{password}@{server_host}:{port}/{db}")
    engine_url = pg_engine.url
    for table in tables:
        pg_engine.logging_name = "ProcessLogger"
        pg_engine.logger.setLevel(WARNING)
        working_df = oguri_utils.read_database(f"SELECT * FROM {table}", ENGINE)  # noqa: S608

        full_table = f"{schema}.{table}" if schema else table

        working_df.write_database(full_table, engine_url, if_table_exists="replace")

    pg_engine.dispose()


app = typer.Typer(name="JP Text Interface")


@app.command()
def to_pg(
    username: str, password: str, server_host: str, port: int, db: str, schema: Optional[str] = None  # noqa: UP007
) -> None:
    """
    Extracts the data and set tables from the SQLite DB and inserts them into the provided PostgreSQL Instance.

    Args:\n
        username: PostgreSQL username\n
        password: <PASSWORD>\n
        server_host: PostgreSQL server host\n
        port: PostgreSQL server port\n
        db: PostgreSQL database name\n
        schema: Optional PostgreSQL schema name to write tables into\n
    """
    load_tables_to_pg(username, password, server_host, port, db, schema)


@app.command()
def to_csv() -> None:
    "Extracts the data and set tables from the database to individual CSV files."
    table_to_csv()


if __name__ == "__main__":
    app()
