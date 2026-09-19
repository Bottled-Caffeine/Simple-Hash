from PyQt6.QtWidgets import QVBoxLayout, QWidget

from simple_hash.ui.widgets import CardWidget, MarkdownViewer

from .base_page import BasePage


class HomePage(BasePage):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self._create_widgets()
        self._build_layout()
        self._connect_signals()

    def _create_widgets(self) -> None:
        # Changelog
        self.changelog_card = CardWidget("What's New")

        self.changelog = MarkdownViewer("assets/changelog.md")

    def _build_layout(self) -> None:
        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        layout.addWidget(self.changelog_card)
        layout.addStretch()

        # Changelog card
        self.changelog_card.layout.addWidget(self.changelog)

    def _connect_signals(self) -> None:
        pass
