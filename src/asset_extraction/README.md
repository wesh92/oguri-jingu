# Source Code Documentation

#### Huge shoutout to `rockisch`

Without your work I'd have been shooting in the dark!

This document provides a brief overview of the different files under the `src/asset_extraction` directory.

I've tried to make the code modular and self-documenting. Outside of type hinting you won't find an inordiante amount of commenting in the code. When warranted I encourage any future contributor to feel free to add as much as they deem necessary but let's keep from overdoing it!

## Differences from `umamusu-utils`

- Instead of pulling from the asset remote storage buckets we extract directly from the game files (Uses DMM-based files.).
- Interactive choice on what you want to pull.
- Speedy! (if you want it to be.)

## Requirements

You _must_ have Poetry OR install all of the required deps into your global packages. I specifically _do not_ provide you with a `requirements.txt` because installing into your global packages is not recommended. Using a venv isn't difficult (especially with Poetry) and ensures the script will run as it did on my system. If this becomes needlessly difficult for folks, at some point I may look into containerization.

## main.py

This is the main entry point for the asset extraction process. It uses functions from `oguri_utils.py`, `oguri_processing.py`, and `oguri_interface.py` to extract and process assets. It also uses the `MetaModel` class from `meta_model.py` to represent the metadata of a model such as the folder/file path for the asset.

## oguri_interface.py

This file contains functions for user interaction. It includes a function to confirm if the user wants to proceed with the processing when using the "all" option (`confirm_processing`) and a function to display the main interface (`main_interface`).

## oguri_processing.py

This file contains functions for processing and saving image data (`process_and_save_image_data`) and constructing the full path for a model (`construct_full_path`).

## oguri_utils.py

This file contains utility functions used by other scripts. One of the main functions is `read_config`, which reads the configuration file `read-config.toml`.

## models/meta_model.py

This file contains the `MetaModel` class, which is a Pydantic model for the metadata of the asset. It includes fields for the name, hash, and meta group of the model, as well as a folder key. Folder Key is used both to navigate the file tree and to create image folders in the `data` directory (one level up).

## read-config.toml

This is the configuration file read by `read_config` in `oguri_utils.py`. It contains paths, table names, and queries used by the asset extraction process.

Please refer to the individual files for more detailed information.

## Example Usage

```shell
python main.py
```

The above will start an interactive shell session asking you to choose which assets you'd like to extract. Enter the number of the category you're after. If you choose "All" just be warned that is ~217k assets. It's A LOT of processing.

After you've selected a category the process will ask you how many thread workers to use. If you leave it blank and hit enter it will just use 5 workers.
If you have a UFO computer you can use as many as you want but I saw diminishing returns >50. If you have a run-of-the-mill computer I'd leave it as default or type `1` just to be safe.

The process will run and, when finished, will do a simple call back to let you know it is finished!
