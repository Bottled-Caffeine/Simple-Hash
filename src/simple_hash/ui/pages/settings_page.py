from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QWidget

from simple_hash.settings import Settings
from simple_hash.ui.widgets import CardWidget, Switch

from .base_page import BasePage


class SettingsPage(BasePage):
    theme_changed = pyqtSignal(bool)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.settings = Settings()

        # Maps display titles to Settings attribute names.
        self.settings_map = {
            "Restore window size": "remember_window_size",
            "Dark theme": "dark_theme",
        }

        self._create_widgets()
        self._build_layout()
        self._connect_signals()

    @pyqtSlot(bool)
    def _on_setting_changed(self, checked: bool) -> None:
        sender = self.sender()
        setting = sender.property("setting")

        setattr(self.settings, setting, checked)

        if setting == "dark_theme":
            self.theme_changed.emit(checked)

    def _create_widgets(self) -> None:
        self.settings_card = CardWidget("Settings")

        self.switches = []
        for title, setting in self.settings_map.items():
            switch = Switch(title, True)
            switch.setProperty("setting", setting)
            switch.setChecked(getattr(self.settings, setting))
            self.switches.append(switch)

    def _build_layout(self) -> None:
        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        layout.addWidget(self.settings_card)
        layout.addStretch()

        # Settings card
        ## Layout
        settings_layout = QGridLayout()

        for row in range((len(self.settings_map) + 1) // 2):
            for col in range(2):
                i = row * 2 + col
                if i < len(self.switches):
                    settings_layout.addWidget(self.switches[i], row, col)

        for row in range(settings_layout.rowCount()):
            settings_layout.setRowMinimumHeight(row, 55)

        for col in range(settings_layout.columnCount()):
            settings_layout.setColumnMinimumWidth(col, 300)

        ## Card
        self.settings_card.layout.setContentsMargins(0, 0, 0, 30)
        self.settings_card.layout.addLayout(settings_layout)

    def _connect_signals(self) -> None:
        for switch in self.switches:
            switch.toggled.connect(self._on_setting_changed)
