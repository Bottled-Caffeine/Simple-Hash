import sys
from pathlib import Path

from PyQt6.QtCore import QCoreApplication, QStandardPaths


def app_data_dir() -> Path:
    return (
        Path(
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.GenericDataLocation
            )
        )
        / QCoreApplication.applicationName()
    )


def reports_dir() -> Path:
    path = app_data_dir() / "reports"
    path.mkdir(parents=True, exist_ok=True)

    return path


def resource_path(relative_path: str) -> Path:
    if getattr(sys, "frozen", False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parents[3]

    return base_path / relative_path
