import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import toml
from supabase import Client, create_client

ROOT = Path(__file__).parent.parent.parent
IMAGES_ROOT = Path(ROOT, "data/meta")
configuration = toml.load(r".\utils\supabase\secrets.toml")


def supabase_client(project_url: str, api_key: str) -> Client:
    return create_client(project_url, api_key)


def upload_file(cli: Client, bucket_name: str, local_file_path: str, upload_path: str) -> None:
    # Upload the file to the bucket
    with open(local_file_path, "rb") as file:
        cli.storage.from_(bucket_name).upload(file=file, path=upload_path, file_options={"content-type": "image/png"})


# Upload images with multithreading
def upload_images(cli: Client, bucket_name: str, local_folder_path: str) -> None:
    # Initialize ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        # Walk through the directory
        for dirpath, _dirnames, filenames in os.walk(local_folder_path):
            for filename in filenames:
                if filename.endswith(".png"):  # Check if the file is a PNG image
                    # Construct the relative path from the base directory for PNG files
                    relative_path = os.path.relpath(dirpath, local_folder_path)
                    upload_path = f"{os.path.join(relative_path, filename).replace('\\', '/')}"
                    local_file_path = os.path.join(dirpath, filename)
                    # Submit upload task to the thread pool
                    executor.submit(upload_file, cli, bucket_name, local_file_path, upload_path)


if __name__ == "__main__":
    cli = supabase_client(configuration["SUPABASE_URL"], configuration["SUPABASE_KEY"])
    upload_images(cli, "uma_assets", str(IMAGES_ROOT))
