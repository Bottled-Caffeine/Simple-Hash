from PyQt6.QtCore import QRectF, QSize, Qt, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QPaintEvent, QPainter, QPalette
from PyQt6.QtWidgets import (
    QAbstractButton,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class BaseSwitch(QAbstractButton):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setCheckable(True)
        self.setFixedSize(40, 21)
        self.setObjectName("switch")

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self.isChecked():
            background = self.palette().color(QPalette.ColorRole.WindowText)
        else:
            background = self.palette().color(QPalette.ColorRole.Button)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(background)

        painter.drawRoundedRect(
            QRectF(0, 0, self.width(), self.height()),
            self.height() / 2,
            self.height() / 2,
        )

        # Handle
        margin = 3
        diameter = self.height() - margin * 2

        x = self.width() - diameter - margin if self.isChecked() else margin

        painter.setBrush(Qt.GlobalColor.white)
        painter.drawEllipse(QRectF(x, margin, diameter, diameter))

    def sizeHint(self) -> QSize:
        return self.size()


class Switch(QWidget):
    toggled = pyqtSignal(bool)

    def __init__(
        self,
        text: str | None = None,
        show_status: bool = False,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.text = text
        self.show_status = show_status

        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        self._create_widgets()
        self._build_layout()
        self._connect_signals()

    @pyqtSlot(bool)
    def _toggled(self, checked: bool) -> None:
        self.toggled.emit(checked)

    def setChecked(self, checked: bool) -> None:
        self.switch.setChecked(checked)

    def isChecked(self) -> bool:
        return self.switch.isChecked()

    def _create_widgets(self) -> None:
        self.switch = BaseSwitch()

        if self.text:
            self.option = QLabel(self.text)

        if self.show_status:
            self.status = QLabel("Off")

    def _build_layout(self) -> None:
        # Content layout
        layout = QHBoxLayout()
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(self.switch)
        if self.show_status:
            layout.addWidget(self.status)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(8)

        if self.text:
            main_layout.addWidget(self.option)

        main_layout.addLayout(layout)

    def _connect_signals(self) -> None:
        self.switch.toggled.connect(
            lambda checked: (
                self.status.setText("On" if checked else "Off")
                if self.show_status
                else None
            )
        )
        self.switch.toggled.connect(self._toggled)
