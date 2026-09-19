from typing import Any

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt

from simple_hash.domain import ReportManifest
from simple_hash.ui.styles import load_icon


class ReportManifestModel(QAbstractTableModel):
    ManifestRole = Qt.ItemDataRole.UserRole + 1

    def __init__(self, manifests: list[ReportManifest]) -> None:
        super().__init__()

        self.manifests = manifests
        self.headers = [
            "",
            "Date",
            "Status",
            "Algorithm",
            "First Manifest",
            "Second Manifest",
        ]

    def rowCount(self, parent: QModelIndex) -> int:
        return len(self.manifests)

    def columnCount(self, parent: QModelIndex) -> int:
        return len(self.headers)

    def data(self, index: QModelIndex, role: int) -> Any:
        if not index.isValid():
            return None

        manifest = self.manifests[index.row()]

        if role == self.ManifestRole:
            return manifest

        if role == Qt.ItemDataRole.DisplayRole:

            match index.column():
                case 1:
                    return manifest.date
                case 2:
                    return "Validated" if not manifest.has_issues else "Has Issues"
                case 3:
                    return manifest.algorithm
                case 4:
                    return manifest.manifest_1
                case 5:
                    return manifest.manifest_2

        if role == Qt.ItemDataRole.TextAlignmentRole:
            if index.column() in (0, 2, 3):
                return Qt.AlignmentFlag.AlignCenter

        if role == Qt.ItemDataRole.DecorationRole:
            if index.column() == 2:
                return (
                    load_icon("assets/icons/table/shield-exclamation.svg")
                    if manifest.has_issues
                    else load_icon("assets/icons/table/shield-check.svg")
                )

        if role == Qt.ItemDataRole.CheckStateRole and index.column() == 0:
            return (
                Qt.CheckState.Checked if manifest.checked else Qt.CheckState.Unchecked
            )

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int,
    ) -> str | None:

        if role != Qt.ItemDataRole.DisplayRole:
            return None

        if orientation == Qt.Orientation.Horizontal:
            return self.headers[section]

    def sort(self, column: int, order: Qt.SortOrder) -> None:
        reverse = order == Qt.SortOrder.DescendingOrder

        key_funcs = {
            0: lambda m: m.checked,
            1: lambda m: m.date,
            2: lambda m: m.has_issues,
            3: lambda m: m.algorithm,
            4: lambda m: m.manifest_1,
            5: lambda m: m.manifest_2,
        }

        self.layoutAboutToBeChanged.emit()
        self.manifests.sort(key=key_funcs[column], reverse=reverse)
        self.layoutChanged.emit()

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        flags = super().flags(index)

        if index.column() == 0:
            flags |= Qt.ItemFlag.ItemIsUserCheckable

        return flags

    def setData(self, index: QModelIndex, value: Any, role: int) -> bool:
        if role == Qt.ItemDataRole.CheckStateRole and index.column() == 0:
            manifest = self.manifests[index.row()]
            manifest.checked = bool(value)

            self.dataChanged.emit(index, index, [Qt.ItemDataRole.CheckStateRole])
            return True

        return False

    def set_manifests(self, manifests: list[ReportManifest]) -> None:
        self.beginResetModel()
        self.manifests = manifests
        self.endResetModel()
