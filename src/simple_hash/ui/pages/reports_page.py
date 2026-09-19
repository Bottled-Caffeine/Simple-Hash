import json

from PyQt6.QtCore import (
    QFileSystemWatcher,
    QModelIndex,
    QCoreApplication,
    Qt,
    pyqtSlot,
)
from PyQt6.QtWidgets import QMessageBox, QVBoxLayout, QWidget

from simple_hash.models import ReportManifestModel
from simple_hash.services import ReportManifestLoader, reports_dir
from simple_hash.ui.dialogs import ReportDialog
from simple_hash.ui.messages import DeleteMessage
from simple_hash.ui.views import ReportsTable
from simple_hash.ui.widgets import BottomBar, CardWidget

from .base_page import BasePage


class ReportsPage(BasePage):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.model = ReportManifestModel(
            ReportManifestLoader.load_manifests(reports_dir())
        )
        self.watcher = QFileSystemWatcher([str(reports_dir())])

        self._create_widgets()
        self._build_layout()
        self._connect_signals()

    @pyqtSlot()
    def _reload_manifests(self) -> None:
        manifests = ReportManifestLoader.load_manifests(reports_dir())
        self.model.set_manifests(manifests)

    @pyqtSlot(QModelIndex)
    def _open_report(self, index: QModelIndex) -> None:
        manifest = index.data(ReportManifestModel.ManifestRole)

        with open(manifest.path) as f:
            report = json.load(f)

        reports_dialog = ReportDialog(report)
        reports_dialog.exec()

    @pyqtSlot()
    def _update_delete_enabled(self, *args) -> None:
        enabled = any(manifest.checked for manifest in self.model.manifests)
        self.bottom_bar.button.setEnabled(enabled)

    @pyqtSlot()
    def _process(self) -> None:
        self.bottom_bar.button.setEnabled(False)
        self.bottom_bar.button.setText("Processing...")
        QCoreApplication.processEvents()

        message = DeleteMessage(self)

        message.exec()

        try:
            if message.clickedButton() == message.continue_button:
                self._delete_reports()
            else:
                self._update_delete_enabled()

        finally:
            self.bottom_bar.button.setText("Delete")

    def _delete_reports(self) -> None:
        failed = False
        for manifest in self.model.manifests:
            if not manifest.checked:
                continue

            try:
                manifest.path.unlink()

            except FileNotFoundError:
                pass

            except OSError as e:
                failed = True

        if failed:
            QMessageBox.warning(
                self,
                "Delete failed",
                f"Failed to delete one or more files.",
            )

    def _create_widgets(self) -> None:
        # Table
        self.table_card = CardWidget("Comparison Reports")

        self.table = ReportsTable()
        self.table.setModel(self.model)

        # Bottomm bar
        self.bottom_bar = BottomBar("Delete")

    def _build_layout(self) -> None:
        # Content layout
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(12, 12, 12, 12)
        content_layout.setSpacing(8)

        content_layout.addWidget(self.table_card)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addLayout(content_layout)
        main_layout.addWidget(self.bottom_bar, alignment=Qt.AlignmentFlag.AlignBottom)

        # Table card
        self.table_card.layout.addWidget(self.table)

    def _connect_signals(self) -> None:
        self.watcher.directoryChanged.connect(self._reload_manifests)
        self.table.doubleClicked.connect(self._open_report)
        self.model.dataChanged.connect(self._update_delete_enabled)
        self.model.modelReset.connect(self._update_delete_enabled)
        self.bottom_bar.button.clicked.connect(self._process)

        # Initialize state.
        self._update_delete_enabled()
