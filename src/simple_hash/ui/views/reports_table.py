from PyQt6.QtCore import QAbstractItemModel, QEvent, QModelIndex, Qt
from PyQt6.QtGui import QMouseEvent, QPainter
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QStyle,
    QStyleOptionViewItem,
    QStyledItemDelegate,
    QTableView,
    QWidget,
)


class ReportsTable(QTableView):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setSortingEnabled(True)

        self.delegate = TableDelegate(self)
        self.setItemDelegate(self.delegate)

        self.entered.connect(self.on_entered)

    def setModel(self, model: QAbstractItemModel | None) -> None:
        super().setModel(model)
        self.set_header()

    def set_header(self) -> None:
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

        for column in (1, 4, 5):
            header.setSectionResizeMode(column, QHeaderView.ResizeMode.Stretch)

        for column in (0, 2, 3):
            header.setSectionResizeMode(column, QHeaderView.ResizeMode.ResizeToContents)

    def on_entered(self, index: QModelIndex) -> None:
        self.delegate.hover_row = index.row()
        self.viewport().update()

    def leaveEvent(self, event: QEvent) -> None:
        self.delegate.hover_row = -1
        self.viewport().update()
        super().leaveEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        index = self.indexAt(event.pos())

        if index.isValid() and index.column() == 0:
            event.accept()
            
            return

        super().mouseDoubleClickEvent(event)


class TableDelegate(QStyledItemDelegate):
    def __init__(self, table: QTableView) -> None:
        super().__init__(table)

        self.table = table
        self.hover_row = -1

    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionViewItem,
        index: QModelIndex,
    ) -> None:
        if index.row() == self.hover_row:
            option.state |= QStyle.StateFlag.State_MouseOver
        super().paint(painter, option, index)

    def initStyleOption(
        self,
        option: QStyleOptionViewItem,
        index: QModelIndex,
    ) -> None:
        super().initStyleOption(option, index)
        
        option.decorationAlignment = Qt.AlignmentFlag.AlignCenter
