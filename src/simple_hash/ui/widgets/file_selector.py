from PyQt6.QtCore import QDir, Qt, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class FileSelector(QWidget):
    path_changed = pyqtSignal(str)

    def __init__(
        self,
        label_text: str | None = None,
        placeholder: str = "No file selected.",
        file_filter: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.path = None
        self.label_text = label_text
        self.placeholder = placeholder
        self.file_filter = file_filter

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self._create_widgets()
        self._build_layout()
        self._connect_signals()

    def set_path(self, path: str) -> None:
        self.path = path
        self.line.setText(path)

        self.path_changed.emit(path)

    @pyqtSlot()
    def _select_file(self) -> None:
        file, _ = QFileDialog.getOpenFileName(
            self, "Select File", QDir.homePath(), self.file_filter
        )

        if file:
            self.set_path(file)

    def _create_widgets(self) -> None:
        if self.label_text:
            self.label = QLabel(self.label_text)

        self.button = QPushButton("Browse...")
        self.button.setFixedWidth(120)
        self.button.setFixedHeight(32)

        self.line = QLineEdit()
        self.line.setFixedHeight(32)

        self.line.setReadOnly(True)
        self.line.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.line.setPlaceholderText(self.placeholder)

    def _build_layout(self) -> None:
        # Layout
        layout = QHBoxLayout()

        layout.addWidget(self.line)
        layout.addWidget(self.button)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(6)

        if self.label:
            main_layout.addWidget(self.label)

        main_layout.addLayout(layout)

    def _connect_signals(self) -> None:
        self.button.clicked.connect(self._select_file)
