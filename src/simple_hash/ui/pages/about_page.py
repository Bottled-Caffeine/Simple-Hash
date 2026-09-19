from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from simple_hash.ui.widgets import CardWidget, LinkWidget, MarkdownViewer

from .base_page import BasePage


class AboutPage(BasePage):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self._create_widgets()
        self._build_layout()
        self._connect_signals()

    def update_icons(self) -> None:
        for button in self.buttons:
            button.update_icon()

    def _create_widgets(self) -> None:
        # About
        self.about_card = CardWidget("About")

        self.about = MarkdownViewer("assets/about.md")

        # Links
        self.links_card = CardWidget("Links")

        links_map = {
            "github": {
                "label_text": "GitHub",
                "icon_path": "assets/icons/links/github.svg",
                "url": "https://github.com/Bottled-Caffeine/Simple-Hash",
            },
            "kofi": {
                "label_text": "Ko-Fi",
                "icon_path": "assets/icons/links/ko-fi.svg",
                "url": "https://ko-fi.com/bottled_caffeine",
            },
        }

        self.buttons = []
        for data in links_map.values():
            button = LinkWidget(
                label_text=data["label_text"],
                icon_path=data["icon_path"],
                url=data["url"],
            )
            self.buttons.append(button)

    def _build_layout(self) -> None:
        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        layout.addWidget(self.about_card)
        layout.addWidget(self.links_card)
        layout.addStretch()

        # About card
        self.about_card.layout.addWidget(self.about)

        # Links card
        ## Layout
        links_layout = QHBoxLayout()
        links_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        links_layout.setSpacing(20)

        for button in self.buttons:
            links_layout.addWidget(button)

        ## Card
        self.links_card.layout.setContentsMargins(0, 0, 0, 30)
        self.links_card.layout.addLayout(links_layout)

    def _connect_signals(self) -> None:
        pass
