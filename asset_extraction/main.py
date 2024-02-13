import os
import sys
from concurrent.futures import ThreadPoolExecutor
from logging import CRITICAL, INFO, getLogger

import oguri_interface
import oguri_processing
import UnityPy
from models.meta_model import MetaModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import utils.oguri_utils as oguri_utils

EXTERNAL_CONFIG = oguri_utils.read_config(r".\read-config.toml")
SKIP_EXISTING = True
DATA_ROOT = oguri_utils.get_storage_folder("meta")


def create_engine(config: dict, region: str = "JP"):  # noqa: ANN201
    return oguri_utils.sqlite_connection("meta_db", configuration=config, region=region)


def extract_blob_to_list(blob_name: str | None = None, region: str = "JP") -> list:
    engine = create_engine(EXTERNAL_CONFIG, region=region)
    return (
        oguri_utils.extract_blob_info(region=region, kind=blob_name, engine=engine, config=EXTERNAL_CONFIG)
        .to_struct()
        .to_list()
    )


def create_models(db_list: list) -> list:
    return [MetaModel(**row) for row in db_list]


def process_model(model: MetaModel, region: str = "JP") -> None:
    full_path = oguri_processing.construct_full_path(model, EXTERNAL_CONFIG, region=region)
    env = UnityPy.load(full_path)
    oguri_processing.process_and_save_image_data(env, model, DATA_ROOT)


def main_processing(blob_name: str | None = None, max_workers: int = 5, region: str = "JP") -> None:
    db = extract_blob_to_list(blob_name, region=region)
    models = create_models(db)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(process_model, models, [region] * len(models))


if __name__ == "__main__":
    db_opts = """
        SELECT DISTINCT m FROM a
        """
    region = input("Select region: [JP, KO, TW, ZH] ")
    if region.upper() not in ["JP", "KO", "TW", "ZH"]:
        raise NotImplementedError(f"Region {region} is not supported.")
    engine = create_engine(EXTERNAL_CONFIG, region=region)
    db_options = oguri_utils.read_database(db_opts, engine).to_series().to_list()
    db_options.append("All")  # Add 'All' option to the list
    db_filter, max_workers = oguri_interface.main_interface(db_options)

    if max_workers > 20:
        oguri_interface.confirm_processing(method="many_threads")

    if db_filter == "All":
        if oguri_interface.confirm_processing():
            main_processing(max_workers=max_workers, region=region)
        else:
            getLogger("OpLogger").log(CRITICAL, "Processing aborted by user.")
    else:
        main_processing(db_filter, max_workers=max_workers, region=region)
        getLogger("OpLogger").log(INFO, "Processing complete.")
