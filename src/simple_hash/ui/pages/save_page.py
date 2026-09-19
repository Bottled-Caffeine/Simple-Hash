from PyQt6.QtCore import QCoreApplication, Qt, pyqtSlot
from PyQt6.QtWidgets import (
    QGridLayout,
    QLabel,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from simple_hash.logic import save_hashes
from simple_hash.settings import Settings
from simple_hash.ui.widgets import (
    AlgorithmSelector,
    BottomBar,
    CardWidget,
    DirectorySelector,
    Switch,
)

from .base_page import BasePage


class SavePage(BasePage):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.settings = Settings()

        self._create_widgets()
        self._build_layout()
        self._connect_signals()

    @pyqtSlot(bool)
    @pyqtSlot(str)
    def _on_setting_changed(self, value: bool | str) -> None:
        sender = self.sender()
        setting = sender.property("setting")

        setattr(self.settings, setting, value)

    @pyqtSlot()
    def _update_save_enabled(self, *_args) -> None:
        enabled = bool(self.target_directory.path) and bool(self.save_directory.path)
        self.bottom_bar.button.setEnabled(enabled)

    @pyqtSlot()
    def _process(self) -> None:
        self.bottom_bar.button.setEnabled(False)
        self.bottom_bar.button.setText("Processing...")
        QCoreApplication.processEvents()

        save_hashes(
            self.target_directory.path,
            self.save_directory.path,
            self.algorithm_selector.algorithm,
            self.recursive_switch.isChecked(),
        )

        self.bottom_bar.button.setEnabled(True)
        self.bottom_bar.button.setText("Save")

        QMessageBox.information(
            self, "Complete", f"Hashes saved to:\n{self.save_directory.path}"
        )

    def _create_widgets(self) -> None:
        # Description
        self.description_card = CardWidget()

        self.description = QLabel(
            "Recursively scan a directory, save file relative paths and hashes to a JSON file."
        )
        self.description.setWordWrap(True)

        # Directories
        self.directories_card = CardWidget()

        self.target_directory = DirectorySelector(
            label_text="Target Directory:",
            placeholder="No directory selected.",
        )
        self.target_directory.setMinimumWidth(600)

        self.save_directory = DirectorySelector(
            label_text="Save Directory:",
            placeholder="No directory selected.",
        )
        self.save_directory.setMinimumWidth(600)

        # Options
        self.options_card = CardWidget()

        self.algorithm_selector = AlgorithmSelector(labeled=False)
        self.algorithm_selector.setProperty(
            "setting",
            "algorithm",
        )
        self.algorithm_selector.algorithm = self.settings.algorithm

        self.recursive_switch = Switch()
        self.recursive_switch.setProperty(
            "setting",
            "recursive",
        )
        self.recursive_switch.setChecked(self.settings.recursive)

        # Bottom bar
        self.bottom_bar = BottomBar("Save")

    def _build_layout(self) -> None:
        # Content Layout
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(12, 12, 12, 12)
        content_layout.setSpacing(8)

        content_layout.addWidget(self.description_card)
        content_layout.addWidget(self.directories_card)
        content_layout.addWidget(self.options_card)

        content_layout.addStretch()

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addLayout(content_layout)
        main_layout.addWidget(self.bottom_bar, alignment=Qt.AlignmentFlag.AlignBottom)

        # Description card
        self.description_card.layout.addWidget(self.description)

        # Directories card
        self.directories_card.layout.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
        )
        self.directories_card.layout.setContentsMargins(0, 8, 0, 30)
        self.directories_card.layout.setSpacing(20)

        self.directories_card.layout.addWidget(self.target_directory)
        self.directories_card.layout.addWidget(self.save_directory)

        # Options card
        ## Layout
        options_layout = QGridLayout()
        options_layout.setVerticalSpacing(6)
        options_layout.setHorizontalSpacing(50)

        options_layout.addWidget(
            QLabel("Hash Algorithm"), 0, 0, alignment=Qt.AlignmentFlag.AlignHCenter
        )
        options_layout.addWidget(
            QLabel("Recursive"), 0, 1, alignment=Qt.AlignmentFlag.AlignHCenter
        )
        options_layout.addWidget(
            self.algorithm_selector, 1, 0, alignment=Qt.AlignmentFlag.AlignHCenter
        )
        options_layout.addWidget(
            self.recursive_switch, 1, 1, alignment=Qt.AlignmentFlag.AlignHCenter
        )

        ## Card
        self.options_card.layout.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
        )
        self.options_card.layout.setContentsMargins(0, 8, 0, 30)
        self.options_card.layout.setSpacing(20)

        self.options_card.layout.addLayout(options_layout)

    def _connect_signals(self) -> None:
        self.target_directory.path_changed.connect(self._update_save_enabled)
        self.save_directory.path_changed.connect(self._update_save_enabled)
        self.algorithm_selector.algorithm_changed.connect(self._on_setting_changed)
        self.recursive_switch.toggled.connect(self._on_setting_changed)
        self.bottom_bar.button.clicked.connect(self._process)

        # Initialize state.
        self._update_save_enabled()
