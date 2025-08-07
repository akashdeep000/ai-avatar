import os
import tarfile
import requests
from tqdm import tqdm
from loguru import logger
from urllib.parse import urlparse

def download_and_extract(url: str, output_dir: str):
    """
    Downloads a file from a URL, extracts it if it's a tar archive, and saves it to the output directory.

    Args:
        url (str): The URL of the file to download.
        output_dir (str): The directory to save the extracted files to.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get filename from URL
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    filepath = os.path.join(output_dir, filename)

    # Download the file with a progress bar
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes
        total_size = int(response.headers.get("content-length", 0))

        with open(filepath, "wb") as f, tqdm(
            desc=filename,
            total=total_size,
            unit="iB",
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=1024):
                size = f.write(data)
                bar.update(size)
        logger.info(f"Downloaded '{filename}' to '{filepath}'")

        # Extract the file if it's a tar archive
        if tarfile.is_tarfile(filepath):
            with tarfile.open(filepath, "r:*") as tar:
                tar.extractall(path=output_dir)
            logger.info(f"Extracted '{filename}' to '{output_dir}'")
            os.remove(filepath)  # Clean up the archive file
        else:
            logger.warning(f"'{filename}' is not a tar archive. Skipping extraction.")

    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading file: {e}")
    except tarfile.TarError as e:
        logger.error(f"Error extracting tar file: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

def download_file(url: str, output_dir: str):
    """
    Downloads a file from a URL and saves it to the output directory.

    Args:
        url (str): The URL of the file to download.
        output_dir (str): The directory to save the file to.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    filepath = os.path.join(output_dir, filename)

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get("content-length", 0))

        with open(filepath, "wb") as f, tqdm(
            desc=filename,
            total=total_size,
            unit="iB",
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=1024):
                size = f.write(data)
                bar.update(size)
        logger.info(f"Downloaded '{filename}' to '{filepath}'")

    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading file: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

def check_and_extract_local_file(url: str, output_dir: str) -> str | None:
    """
    Checks if a local file corresponding to the URL's filename exists in the output directory.
    If it exists and is a tar file, it extracts it.

    Args:
        url (str): The URL to derive the filename from.
        output_dir (str): The directory to check for the file in.

    Returns:
        str | None: The path to the local file if found, otherwise None.
    """

    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    filepath = os.path.join(output_dir, filename)

    if os.path.exists(filepath):
        logger.info(f"Local file found: {filepath}")
        if tarfile.is_tarfile(filepath):
            try:
                with tarfile.open(filepath, "r:*") as tar:
                    tar.extractall(path=output_dir)
                logger.info(f"Extracted '{filename}' to '{output_dir}'")
                os.remove(filepath)
                return filepath
            except tarfile.TarError as e:
                logger.error(f"Error extracting tar file: {e}")
                return None
        else:
            logger.warning(
                f"'{filename}' is not a tar archive. Skipping extraction."
            )
            return filepath
    return None
