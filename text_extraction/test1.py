import os
import sys
from logging import WARNING, getLogger

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import utils.oguri_utils as oguri_utils

EXTERNAL_CONFIG = oguri_utils.read_config(r"text_extraction\config.toml")
ENGINE = oguri_utils.sqlite_connection("master_db", configuration=EXTERNAL_CONFIG)


def table_to_csv(config: dict, search_table: str) -> None:
    working_config = config["table_relation_ids"][0]
    table_config = working_config[search_table]
    print(table_config)  # noqa: T201
    getLogger("ProcessLogger").log(WARNING, f"Extracting table: {working_config}")
    # Query the table for ALL data and insert into polars df
    working_df = oguri_utils.read_database(f"SELECT * FROM {working_config}", ENGINE)  # noqa: S608
    working_df.write_csv(f"../data/{working_config}.csv")


table_to_csv(EXTERNAL_CONFIG, "item_groups")
