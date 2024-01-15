from logging import DEBUG, getLogger
from pathlib import Path
from typing import Any

import polars as pl
import toml
from sqlalchemy import Engine, create_engine

system_logger = getLogger("SysLogger")

ROOT = Path(__file__).parent.parent  # Goes 2 levels up from this file to \src
system_logger.log(DEBUG, f"ROOT: {ROOT}")
STORAGE_ROOT = Path(ROOT, "data")
system_logger.log(DEBUG, f"STORAGE_ROOT: {STORAGE_ROOT}")


def get_storage_folder(folder: str) -> Path:
    """
    Gets the storage folder for the specified folder.

    Args:
        folder (`str`): The folder to get the storage path for.

    Returns:
        `Path`: The path to the storage folder.
    """
    path = Path(STORAGE_ROOT, folder)
    path.mkdir(exist_ok=True)
    return path


def read_config() -> dict[str, Any]:
    """Reads the config file.

    Path: `src/read-config.toml`

    Returns:
        `dict[str, Any]`: The config file as a dictionary.
            Refer to the config file for the structure.
    """
    return toml.load(r"src\asset_extraction\read-config.toml")


def sqlite_connection(execution_db: str, config: dict[str, Any] = read_config()) -> Engine:
    """Creates a connection to the SQLite database.

    Args:
        execution_db (`str`): The name of the database to connect to.
            This is the key of the database in the config file.
            Choices: `master_db`, `meta_db`
        config (`dict[str, Any]`): The config file as a dictionary.
            Refer to the config file for the structure.

    Returns:
        `sqlite3.Connection`: The connection to the database.
    """
    db_base_path = Path(config["paths"]["win_path"]).expanduser()
    sqlite_db_path = str(db_base_path / config["paths"][execution_db])
    system_logger.log(DEBUG, f"sqlite_db_path: {sqlite_db_path}")
    conn = create_engine("sqlite:///" + sqlite_db_path)
    return conn


def read_database(query: str, conn: Engine) -> pl.DataFrame:
    """Reads the database.

    Args:
        query (`str`): The query to run on the database.
        conn (`Engine`): The Engine to be used connecting to the database.

    Returns:
        `pl.DataFrame`: The data from the database.
    """
    return pl.read_database(query, conn)


def extract_blob_info(kind: str | None = None, engine: Engine = None) -> pl.DataFrame:
    """Extracts the meta blob information from the database.

    Returns:
        `pl.DataFrame`: The meta information from the database.
    """
    config = read_config()
    if kind is not None:
        query = f"""
        SELECT {config['meta_tables']['blob_table_PATH']},
        {config['meta_tables']['blob_table_HASH']},
        {config['meta_tables']['blob_table_KIND']}
        FROM {config['meta_tables']['blob_table']}
        WHERE {config['meta_tables']['blob_table_KIND']} = '{kind}';"""  # noqa: S608
    else:
        query = f"""
        SELECT {config['meta_tables']['blob_table_PATH']},
        {config['meta_tables']['blob_table_HASH']},
        {config['meta_tables']['blob_table_KIND']}
        FROM {config['meta_tables']['blob_table']};"""  # noqa: S608

    return read_database(query, engine)
