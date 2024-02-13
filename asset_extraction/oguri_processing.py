import os
import pathlib

import UnityPy.environment
from pydantic import BaseModel


def process_and_save_image_data(env: UnityPy.environment, model: BaseModel, root_data_folder: pathlib.Path) -> None:
    """
    Extracts the image data from the UnityPy environment and saves it to the
    specified location.

    NOTE: Limited to Texture2D objects (until needed otherwise).

    Args
        `env` : UnityPy.environment
            The UnityPy environment containing the data to be extracted.
        `model` : oguri_processing.Model
            The model containing the data to be extracted.
        `root_data_folder` : pathlib.Path
            The root folder to save the extracted data to.

    Returns
    ```python
        None
    ```
    """
    for obj in env.objects:
        if obj.type.name in ["Texture2D", "Sprite"]:
            data = obj.read()

            dest = root_data_folder / model.region / model.meta_group / data.name
            dest.parent.mkdir(parents=True, exist_ok=True)

            dest = dest.with_suffix(".png")

            img = data.image
            img.save(dest)


def construct_full_path(model: BaseModel, configuration: dict, region: str) -> str:
    """
    Constructs the full path to the asset.

    Args:
        `model` : oguri_processing.Model
            The model containing the data to be extracted.
        `configuration` : dict
            The configuration file.
        `region` : str
            The region to use.
            Choices: `JP`, `KO`, `TW`, `ZH`, default: `JP`
    Returns:
        `str`: The full path to the asset.
    """
    if region.upper() == "JP":
        assets_path = configuration["paths"]["win_path_jp"]
    elif region.upper() == "KO":
        assets_path = configuration["paths"]["win_path_ko"]
    elif region.upper() == "TW" or region == "ZH":
        assets_path = configuration["paths"]["win_path_tw"]
    else:
        NotImplementedError(f"Region {region} is not supported.")
    return os.path.join(
        os.path.expanduser(assets_path),
        configuration["paths"]["asset_path"],
        model.folder_key,
        model.asset_hash,
    )
