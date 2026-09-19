from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget


class BasePage(QWidget):
    switch_page = pyqtSignal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setObjectName("page")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
