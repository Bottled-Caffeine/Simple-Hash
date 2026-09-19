from PyQt6.QtCore import QCoreApplication, Qt, pyqtSlot
from PyQt6.QtWidgets import QLabel, QMessageBox, QVBoxLayout, QWidget

from simple_hash.domain import ValidationError
from simple_hash.logic import compare_hashes
from simple_hash.services import reports_dir, save_json
from simple_hash.ui.dialogs import ReportDialog
from simple_hash.ui.widgets import BottomBar, CardWidget, FileSelector

from .base_page import BasePage


class ComparePage(BasePage):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self._create_widgets()
        self._build_layout()
        self._connect_signals()

    @pyqtSlot()
    def _update_compare_enabled(self, *_args) -> None:
        enabled = bool(self.first_manifest.path) and bool(self.second_manifest.path)
        self.bottom_bar.button.setEnabled(enabled)

    @pyqtSlot()
    def _process(self) -> None:
        self.bottom_bar.button.setEnabled(False)
        self.bottom_bar.button.setText("Processing...")

        QCoreApplication.processEvents()

        try:
            report, timestamp = compare_hashes(
                self.first_manifest.path,
                self.second_manifest.path,
            )

        except ValidationError as e:
            QMessageBox.critical(
                self,
                "Invalid files",
                str(e),
            )

            return

        finally:
            self.bottom_bar.button.setEnabled(True)
            self.bottom_bar.button.setText("Compare")

        save_json(reports_dir(), "report", report, timestamp)

        if not report["metadata"]["has_issues"]:
            QMessageBox.information(
                self,
                "Complete",
                "No difference found, files are identical.",
            )

        else:
            QMessageBox.information(
                self,
                "Complete",
                "Differences found, displaying report.",
            )

        report_dialog = ReportDialog(report)
        report_dialog.exec()

    def _create_widgets(self) -> None:
        # Description
        self.description_card = CardWidget()
        self.description = QLabel(
            "Compare two hash manifests, generating a report of missing folders, missing files, and files with mismatched."
        )
        self.description.setWordWrap(True)

        # File selectors
        self.files_card = CardWidget()

        self.first_manifest = FileSelector(
            label_text="First Manifest:",
            placeholder="No manifest selected.",
            file_filter="JSON Files (*.json)",
        )
        self.first_manifest.setMinimumWidth(600)

        self.second_manifest = FileSelector(
            label_text="Second Manifest:",
            placeholder="No manifest selected.",
            file_filter="JSON Files (*.json)",
        )
        self.second_manifest.setMinimumWidth(600)

        # Bottom bar
        self.bottom_bar = BottomBar("Compare")

    def _build_layout(self) -> None:
        # Content layout
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(12, 12, 12, 12)
        content_layout.setSpacing(8)

        content_layout.addWidget(self.description_card)
        content_layout.addWidget(self.files_card)
        content_layout.addStretch()

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addLayout(content_layout)
        main_layout.addWidget(self.bottom_bar, alignment=Qt.AlignmentFlag.AlignBottom)

        # Description card
        self.description_card.layout.addWidget(self.description)

        # Files card
        self.files_card.layout.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
        )
        self.files_card.layout.setContentsMargins(0, 8, 0, 30)
        self.files_card.layout.setSpacing(20)

        self.files_card.layout.addWidget(
            self.first_manifest,
        )
        self.files_card.layout.addWidget(
            self.second_manifest,
        )

    def _connect_signals(self) -> None:
        self.first_manifest.path_changed.connect(self._update_compare_enabled)
        self.second_manifest.path_changed.connect(self._update_compare_enabled)
        self.bottom_bar.button.clicked.connect(self._process)

        # Initialize state.
        self._update_compare_enabled()
