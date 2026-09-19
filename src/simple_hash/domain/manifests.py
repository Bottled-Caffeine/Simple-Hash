from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(slots=True)
class ReportManifest:
    path: Path
    app_name: str
    version: str
    date: datetime
    algorithm: str
    manifest_1: str
    manifest_2: str
    has_issues: bool
    checked: bool = False


@dataclass(slots=True)
class HashManifest:
    path: Path
    app_name: str
    version: str
    date: datetime
    target_directory: str
    algorithm: str
    recursive: bool
    hashes: dict[str, dict[str, str]]

    @property
    def manifest_name(self) -> str:
        return self.path.name
