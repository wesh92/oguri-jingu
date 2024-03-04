from logging import DEBUG, WARNING, getLogger
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


def read_config(toml_path: str) -> dict[str, Any]:
    """Reads the config file.

    Args:
        toml_path (`str`): The path to the config file.

    Returns:
        `dict[str, Any]`: The config file as a dictionary.
    """
    return toml.load(toml_path)


def sqlite_connection(execution_db: str, configuration: dict[str, Any] | None = None, region: str | None = None) -> Engine:
    """Creates a connection to the SQLite database.

    Args:
        execution_db (`str`): The name of the database to connect to.
            This is the key of the database in the config file.
            Choices: `master_db`, `meta_db`
        configuration (`dict[str, Any]`): The config file as a dictionary.
            Refer to the config file for the structure.
        region (`str`): The region of the game.
            Choices: `JP`, `KO`, `TW`, `ZH`, default: `JP`

    Returns:
        `sqlite3.Connection`: The connection to the database.
    """
    if region is None or region.upper() == "JP":
        assets_path = configuration["paths"]["win_path_jp"]
    elif region.upper() == "KO":
        assets_path = configuration["paths"]["win_path_ko"]
    elif region.upper() == "TW" or region == "ZH":
        assets_path = configuration["paths"]["win_path_tw"]
    else:
        NotImplementedError(f"Region {region} is not supported.")
    db_base_path = Path(assets_path).expanduser()
    sqlite_db_path = str(db_base_path / configuration["paths"][execution_db])
    system_logger.log(WARNING, f"Base Path: {db_base_path}")
    system_logger.log(WARNING, f"sqlite_db_path: {sqlite_db_path}")
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


def extract_blob_info(
    region: str, kind: str | None = None, engine: Engine = None, config: dict[str, Any] | None = None
) -> pl.DataFrame:
    """Extracts the meta blob information from the database.

    Returns:
        `pl.DataFrame`: The meta information from the database.
    """
    if kind is not None:
        query = f"""
        SELECT {config['meta_tables']['blob_table_PATH']},
        {config['meta_tables']['blob_table_HASH']},
        {config['meta_tables']['blob_table_KIND']},
        "{region}" AS region
        FROM {config['meta_tables']['blob_table']}
        WHERE {config['meta_tables']['blob_table_KIND']} = '{kind}';"""  # noqa: S608
    else:
        query = f"""
        SELECT {config['meta_tables']['blob_table_PATH']},
        {config['meta_tables']['blob_table_HASH']},
        {config['meta_tables']['blob_table_KIND']},
        "{region}" AS region
        FROM {config['meta_tables']['blob_table']};"""  # noqa: S608

    return read_database(query, engine)
