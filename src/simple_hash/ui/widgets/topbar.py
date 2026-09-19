from PyQt6.QtCore import QSize, Qt, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QToolButton, QWidget

from simple_hash.services import resource_path


class TopBar(QWidget):
    switch_page = pyqtSignal(str)

    def __init__(
        self,
        *page_names: str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.page_names = page_names

        self.setFixedHeight(30)
        self.setObjectName("topbar")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self._create_widgets()
        self._build_layout()
        self._connect_signals()

    @pyqtSlot()
    def _on_button_clicked(self) -> None:
        button = self.sender()
        page_name = button.property("page_name")
        self.switch_page.emit((page_name).lower())

    def _create_widgets(self) -> None:
        self.label = QLabel("Simple Hash")
        self.label.setObjectName("topbar_title")

        if self.page_names:
            self.buttons = []
            for page_name in self.page_names:
                button = QToolButton()
                button.setFixedSize(20, 20)

                button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
                button.setIcon(
                    QIcon(
                        str(resource_path(f"assets/icons/nav/{page_name.lower()}.svg"))
                    )
                )
                button.setIconSize(QSize(20, 20))

                button.setProperty("page_name", page_name)
                self.buttons.append(button)

    def _build_layout(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 15, 0)

        layout.addWidget(self.label)
        layout.addStretch()
        if self.page_names:
            for button in self.buttons:
                layout.addWidget(button)

    def _connect_signals(self) -> None:
        if self.page_names:
            for button in self.buttons:
                button.clicked.connect(self._on_button_clicked)
