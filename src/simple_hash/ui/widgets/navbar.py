from PyQt6.QtCore import QModelIndex, QSize, Qt, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import (
    QListWidget,
    QListWidgetItem,
    QStyleOptionViewItem,
    QStyledItemDelegate,
    QWidget,
)

from simple_hash.ui.styles import load_icon


class NavBar(QListWidget):
    switch_page = pyqtSignal(str)

    def __init__(
        self,
        *page_names: str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.page_names = page_names

        self.setObjectName("navbar")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setItemDelegate(NavDelegate(self))

        self.setFixedWidth(180)
        self.setIconSize(QSize(20, 20))

        for page_name in page_names:
            icon = load_icon(f"assets/icons/nav/{page_name.lower()}.svg")
            item = QListWidgetItem(icon, page_name)
            self.addItem(item)

        self.currentItemChanged.connect(self._on_item_changed)
        self.setCurrentRow(0)

    @pyqtSlot(QListWidgetItem, QListWidgetItem)
    def _on_item_changed(
        self,
        current: QListWidgetItem | None,
        previous: QListWidgetItem | None,
    ) -> None:
        if current:
            page_name = current.text().lower()
            self.switch_page.emit(page_name)

    def update_state(self, name: str) -> None:
        item = self.findItems(name.capitalize(), Qt.MatchFlag.MatchExactly)
        if not item:
            self.setCurrentItem(None)
            self.clearFocus()

    def update_icons(self) -> None:
        for i, page_name in enumerate(self.page_names):
            icon = load_icon(
                f"assets/icons/nav/{page_name.lower()}.svg",
            )
            self.item(i).setIcon(icon)


class NavDelegate(QStyledItemDelegate):
    def sizeHint(
        self,
        option: QStyleOptionViewItem,
        index: QModelIndex,
    ) -> QSize:
        size = super().sizeHint(option, index)
        size.setHeight(60)

        return size

