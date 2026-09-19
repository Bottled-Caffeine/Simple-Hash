from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget


class CardWidget(QFrame):
    def __init__(
        self,
        title: str | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName("card")
        self.title = title

        self._create_widgets()
        self._build_layout()

    def _create_widgets(self) -> None:
        if self.title:
            self.label = QLabel(self.title)
            self.label.setObjectName("card_title")

    def _build_layout(self) -> None:
        # Content Layout
        self.layout = QVBoxLayout()

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        if self.title:
            main_layout.addWidget(self.label)
            self.label.setAlignment(
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop
            )

        main_layout.addLayout(self.layout)
