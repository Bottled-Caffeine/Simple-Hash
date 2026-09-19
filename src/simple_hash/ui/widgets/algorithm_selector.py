from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class AlgorithmSelector(QWidget):
    algorithm_changed = pyqtSignal(str)

    def __init__(
        self,
        labeled: bool = True,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.labeled = labeled

        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        self._create_widgets()
        self._build_layout()
        self._connect_signals()

    @property
    def algorithm(self) -> str:
        return self.combo_box.currentText()

    @algorithm.setter
    def algorithm(self, value: str) -> None:
        self.combo_box.setCurrentText(value)

    def _create_widgets(self) -> None:
        if self.labeled:
            self.label = QLabel("Hash Algorithm")

        algorithms = ["MD5", "SHA1", "SHA256", "SHA512"]

        self.combo_box = QComboBox()
        self.combo_box.setFixedHeight(32)
        self.combo_box.addItems(algorithms)
        self.combo_box.setEditable(False)

    def _build_layout(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        if self.labeled:
            layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.combo_box, alignment=Qt.AlignmentFlag.AlignCenter)

    def _connect_signals(self) -> None:
        self.combo_box.currentTextChanged.connect(self.algorithm_changed.emit)
