from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QWidget


class BottomBar(QWidget):
    def __init__(
        self,
        text: str = "Button",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.text = text

        self.setFixedHeight(50)
        self.setObjectName("bottombar")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self._create_widgets()
        self._build_layout()

    def _create_widgets(self) -> None:
        self.button = QPushButton(self.text)
        self.button.setMinimumWidth(120)
        self.button.setFixedHeight(32)
        self.button.setObjectName("accept")

    def _build_layout(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)

        layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignRight)
