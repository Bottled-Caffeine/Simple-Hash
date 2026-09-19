"""
Hash generation utilities for files in a directory.

This module provides functions to compute cryptographic hashes for files
within a target directory, optionally recursively, and save the results and
associated metadata as JSON.
"""

import hashlib
from datetime import datetime
from pathlib import Path

from PyQt6.QtCore import QCoreApplication

from simple_hash.services import save_json


def save_hashes(
    target_directory: str,
    save_directory: str,
    hash_algo: str,
    recursive: bool = True,
) -> None:
    """
    Compute hashes for all files in `target_directory` using the specified
    hashing algorithm and save the results as a JSON file in `save_directory`.

    Parameters
    ----------
    target_directory : str
        Path to the directory whose files should be hashed.
    save_directory : str
        Path to the directory where the generated hash manifest should be
        saved.
    hash_algo : str
        Name of the hashing algorithm supported by `hashlib`.
    recursive : bool, default=True
        Whether to recursively include files from subdirectories of
        `target_directory`, optional.
    """

    target_directory = Path(target_directory)
    save_name = f"{target_directory.name}_{hash_algo}".replace(" ", "_")

    timestamp = datetime.now()

    data = {
        "metadata": {
            "app_name": QCoreApplication.applicationName(),
            "version": QCoreApplication.applicationVersion(),
            "date": timestamp.isoformat(timespec="seconds"),
            "target_directory": target_directory.name,
            "algorithm": hash_algo,
            "recursive": recursive,
        },
        "hashes": {},
    }

    # Iterate through all files.
    for entry in (
        target_directory.rglob("*") if recursive else target_directory.glob("*")
    ):
        if entry.is_file():
            folder = entry.parent.relative_to(target_directory).as_posix()
            file_hash = _get_file_hash(entry, hash_algo)

            if folder not in data["hashes"]:
                data["hashes"][folder] = {}

            data["hashes"][folder][entry.name] = file_hash

    # Save to JSON.
    save_json(save_directory, save_name, data, timestamp)


def _get_file_hash(file_path: Path, hash_algo: str) -> str:
    """
    Compute and return the hexadecimal digest of a file using the specified
    hashing algorithm.

    Parameters
    ----------
    file_path : Path
        Path to the file to hash.
    hash_algo : str
        Name of the hashing algorithm supported by `hashlib`.

    Returns
    -------
    str
        The hexadecimal digest of the specified file.
    """

    hash = hashlib.new(hash_algo)

    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hash.update(chunk)

    return hash.hexdigest()
