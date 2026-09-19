"""
Hash manifest comparison utilities.

This module provides a function to compare two hash manifests, validate that
they were generated using compatible settings, and produce a report describing
missing folders, missing files, and hash mismatches.
"""

from datetime import datetime
from pathlib import Path

from PyQt6.QtCore import QCoreApplication

from simple_hash.domain import ValidationError
from simple_hash.services import HashManifestLoader


def compare_hashes(
    path_1: str,
    path_2: str,
) -> tuple[dict, datetime]:
    """
    Load two hash manifests, validate their hashing configuration, compare
    their contents, and return a comparison report with its timestamp.

    Parameters
    ----------
    path_1 : str
        Path to the first hash manifest.
    path_2 : str
        Path to the second hash manifest.

    Returns
    -------
    report : dict
        Comparison report containing metadata and lists of missing folders,
        missing files, and files whose hashes differ. The metadata includes
        whether any issues were detected.

    timestamp : datetime
        Timestamp indicating when the comparison was performed.

    Raises
    ------
    ValidationError
        If the two manifests use different hash algorithms or different
        recursive directory settings.
    """

    manifest_1 = HashManifestLoader.load_manifest(Path(path_1))
    manifest_2 = HashManifestLoader.load_manifest(Path(path_2))

    # Validation.
    if manifest_1.algorithm != manifest_2.algorithm:
        raise ValidationError("Files use different hash algorithms.")

    if manifest_1.recursive != manifest_2.recursive:
        raise ValidationError("Files use different recursion settings.")

    timestamp = datetime.now()

    report = {
        "metadata": {
            "app_name": QCoreApplication.applicationName(),
            "version": QCoreApplication.applicationVersion(),
            "date": timestamp.isoformat(timespec="seconds"),
            "algorithm": manifest_1.algorithm,
            "recursive": manifest_1.recursive,
            "manifest_1": manifest_1.manifest_name,
            "manifest_2": manifest_2.manifest_name,
            "has_issues": False,
        },
        "missing_folders": [],
        "missing_files": [],
        "hash_mismatches": [],
    }

    hashes_1, hashes_2 = manifest_1.hashes, manifest_2.hashes

    # Missing folders.
    for folder in hashes_1.keys() - hashes_2.keys():
        report["missing_folders"].append(
            {
                "folder": folder,
                "reference": manifest_2.manifest_name,
            }
        )

    for folder in hashes_2.keys() - hashes_1.keys():
        report["missing_folders"].append(
            {
                "folder": folder,
                "reference": manifest_1.manifest_name,
            }
        )

    # Compare shared folders.
    for folder in hashes_1.keys() & hashes_2.keys():
        folder_1, folder_2 = hashes_1[folder], hashes_2[folder]

        # Missing files.
        for file in folder_1.keys() - folder_2.keys():
            report["missing_files"].append(
                {
                    "file": file,
                    "folder": folder,
                    "reference": manifest_2.manifest_name,
                }
            )

        for file in folder_2.keys() - folder_1.keys():
            report["missing_files"].append(
                {
                    "file": file,
                    "folder": folder,
                    "reference": manifest_1.manifest_name,
                }
            )

        # Hash mismatches.
        for file in folder_1.keys() & folder_2.keys():
            if folder_1[file] != folder_2[file]:
                report["hash_mismatches"].append(
                    {
                        "file": file,
                        "folder": folder,
                    }
                )

    if any(
        report[entry]
        for entry in (
            "missing_folders",
            "missing_files",
            "hash_mismatches",
        )
    ):
        report["metadata"]["has_issues"] = True

    return report, timestamp
