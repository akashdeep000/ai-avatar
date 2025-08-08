import os
import requests
import tarfile
from pathlib import Path
from tqdm import tqdm
from loguru import logger

def download_and_extract(url: str, output_dir: str) -> Path:
    """
    Download a file from a URL and extract it if it is a tar.bz2 archive.

    Args:
        url (str): The URL to download the file from.
        output_dir (str): The directory to save the downloaded file.

    Returns:
        Path: Path to the extracted directory if it's a tar.bz2 file,
             otherwise Path to the downloaded file.
    """
    # Create the output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Get the file name from the URL
    file_name = url.split("/")[-1]
    file_path = os.path.join(output_dir, file_name)

    # Extract the root directory name from the filename (removing .tar.bz2)
    root_dir = file_name.replace(".tar.bz2", "")
    extracted_dir_path = Path(output_dir) / root_dir

    # Check if the extracted directory already exists
    if extracted_dir_path.exists():
        logger.info(
            f"✅ The directory {extracted_dir_path} already exists. I would assume that the model is already downloaded and we are ready to go. Skipping download and extraction."
        )
        return extracted_dir_path

    # Download the file
    logger.info(f"🏃‍♂️Downloading {url} to {file_path}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an error for bad status codes
    total_size = int(response.headers.get("content-length", 0))
    logger.debug(f"Total file size: {total_size / 1024 / 1024:.2f} MB")

    with (
        open(file_path, "wb") as f,
        tqdm(
            desc=file_name,
            total=total_size,
            unit="iB",
            unit_scale=True,
            unit_divisor=1024,
        ) as pbar,
    ):
        for chunk in response.iter_content(chunk_size=8192):
            size = f.write(chunk)
            pbar.update(size)

    logger.info(f"Downloaded {file_name} successfully.")

    # Extract the tar.bz2 file
    if file_name.endswith(".tar.bz2"):
        logger.info(f"Extracting {file_name}...")
        with tarfile.open(file_path, "r:bz2") as tar:
            members = tar.getmembers()
            for member in tqdm(members, desc=f"Extracting {file_name}"):
                tar.extract(member, path=output_dir)
        logger.info("Extraction completed.")

        # Delete the compressed file
        os.remove(file_path)
        logger.debug(f"Deleted the compressed file: {file_name}")

        return extracted_dir_path
    else:
        logger.warning("The downloaded file is not a tar.bz2 archive.")
        return Path(file_path)


def check_and_extract_local_file(url: str, output_dir: str) -> Path | None:
    """
    Check if a local file exists and extract it if it is a tar.bz2 archive.

    Args:
        url (str): The URL of the file.
        output_dir (str): The directory to save the extracted files.

    Returns:
        Path | None: Path to the extracted directory if it's a tar.bz2 file,
            otherwise None.
    """
    # Get the file name from the URL
    file_name = url.split("/")[-1]
    compressed_path = Path(output_dir) / file_name

    # Check if the compressed file exists and is a tar.bz2 archive
    extracted_dir = Path(output_dir) / file_name.replace(".tar.bz2", "")

    if extracted_dir.exists():
        logger.info(
            f"✅ Extracted directory exists: {extracted_dir}, no operation needed."
        )
        return extracted_dir

    if compressed_path.exists() and file_name.endswith(".tar.bz2"):
        logger.info(f"🔍 Found local archive file: {compressed_path}")

        try:
            logger.info("⏳ Extracting archive file...")
            with tarfile.open(compressed_path, "r:bz2") as tar:
                members = tar.getmembers()
                for member in tqdm(members, desc=f"Extracting {file_name}"):
                    tar.extract(member, path=output_dir)
            logger.success(f"Extracted archive to the path: {extracted_dir}")
            os.remove(compressed_path)  # Remove the compressed file
            return extracted_dir
        except Exception as e:
            logger.error(f"Fail to extract file: {str(e)}")
            return None

    logger.warning(f"Local file not found or not a tar.bz2 archive: {compressed_path}")
    return None