import webbrowser

from PyQt6.QtCore import QSize, Qt, pyqtSlot
from PyQt6.QtWidgets import (
    QLabel,
    QSizePolicy,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from simple_hash.ui.styles import load_icon


class LinkWidget(QWidget):
    def __init__(
        self,
        label_text: str,
        icon_path: str,
        url: str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.label_text = label_text
        self.icon_path = icon_path
        self.url = url

        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        self._create_widgets()
        self._build_layout()
        self._connect_signals()

    @pyqtSlot()
    def _open_link(self) -> None:
        webbrowser.open(self.url)

    def update_icon(self) -> None:
        self.button.setIcon(load_icon(self.icon_path))

    def _create_widgets(self) -> None:
        self.button = QToolButton()
        self.button.setFixedSize(30, 30)
        self.button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.button.setIcon(load_icon(self.icon_path))
        self.button.setIconSize(QSize(30, 30))

        self.label = QLabel(self.label_text)

    def _build_layout(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)

    def _connect_signals(self) -> None:
        self.button.clicked.connect(self._open_link)
