from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QDialog,
    QPushButton,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from simple_hash.services import format_report, resource_path


class ReportDialog(QDialog):
    def __init__(self, report: dict, parent: QWidget | None = None):
        super().__init__(parent)

        self.setWindowTitle("Report — Simple Hash")
        self.setWindowIcon(QIcon(str(resource_path("assets/icons/app/app.svg"))))
        self.resize(650, 450)
        self.setMinimumSize(650, 450)

        self.report = report

        self._create_widgets()
        self._build_layout()
        self._connect_signals()

    def _create_widgets(self):
        self.text = QTextBrowser()
        self.text.setHtml(format_report(self.report))

        self.close_button = QPushButton("Close")
        self.close_button.setObjectName("accept")

    def _build_layout(self):
        layout = QVBoxLayout(self)

        layout.addWidget(self.text)
        layout.addWidget(self.close_button)

    def _connect_signals(self):
        self.close_button.clicked.connect(self.reject)
