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
        if obj.type.name in ["Texture2D"]:
            data = obj.read()

            dest = root_data_folder / model.folder_key / model.asset_hash / data.name
            dest.parent.mkdir(parents=True, exist_ok=True)

            dest = dest.with_suffix(".png")

            img = data.image
            img.save(dest)


def construct_full_path(model: BaseModel, configuration: dict) -> str:
    return os.path.join(
        os.path.expanduser(configuration["paths"]["win_path"]),
        configuration["paths"]["asset_path"],
        model.folder_key,
        model.asset_hash,
    )
