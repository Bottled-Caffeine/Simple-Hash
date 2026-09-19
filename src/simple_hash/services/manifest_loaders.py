import json
from datetime import datetime
from pathlib import Path

from simple_hash.domain import HashManifest, ReportManifest, ValidationError


class ReportManifestLoader:
    @staticmethod
    def load_manifests(directory: Path) -> list[ReportManifest]:
        manifests = []

        for path in directory.glob("*.json"):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                metadata = data["metadata"]

            manifests.append(
                ReportManifest(
                    path=path,
                    app_name=metadata["app_name"],
                    version=metadata["version"],
                    date=datetime.fromisoformat(metadata["date"]),
                    algorithm=metadata["algorithm"],
                    manifest_1=metadata["manifest_1"],
                    manifest_2=metadata["manifest_2"],
                    has_issues=metadata["has_issues"],
                )
            )

        return manifests


class HashManifestLoader:
    @staticmethod
    def load_manifest(directory: Path) -> HashManifest:

        with open(directory, "r", encoding="utf-8") as f:
            data = json.load(f)

            if "metadata" not in data:
                raise ValidationError("Missing metadata section.")

            if "hashes" not in data:
                raise ValidationError("Missing hashes section.")

            metadata = data["metadata"]
            hashes = data["hashes"]

        hash_manifest = HashManifest(
            path=directory,
            app_name=metadata["app_name"],
            version=metadata["version"],
            date=datetime.fromisoformat(metadata["date"]),
            target_directory=metadata["target_directory"],
            algorithm=metadata["algorithm"],
            recursive=metadata["recursive"],
            hashes=hashes,
        )

        return hash_manifest
