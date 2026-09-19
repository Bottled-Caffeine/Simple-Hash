from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QCloseEvent, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from simple_hash.services import resource_path
from simple_hash.settings import Settings
from simple_hash.ui.pages import *
from simple_hash.ui.styles import load_style
from simple_hash.ui.widgets import NavBar, TopBar


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.settings = Settings()

        self.setWindowTitle("Simple Hash")
        self.setWindowIcon(QIcon(str(resource_path("assets/icons/app/app.svg"))))

        if self.settings.remember_window_size:
            self.resize(self.settings.window_size)
        else:
            self.resize(860, 540)

        self.setMinimumSize(860, 540)

        self._create_widgets()
        self._create_pages()
        self._build_layout()
        self._connect_signals()

    @pyqtSlot(str)
    def show_page(self, name: str) -> None:
        self.stack.setCurrentWidget(self.pages[name])
        self.navbar.update_state(name)

    @pyqtSlot()
    def update_theme(self) -> None:
        load_style(QApplication.instance())

        self.navbar.update_icons()
        if page := self.pages.get("about"):
            page.update_icons()

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.settings.remember_window_size:
            self.settings.window_size = self.size()

        super().closeEvent(event)

    def _create_widgets(self) -> None:
        self.stack = QStackedWidget()
        self.topbar = TopBar("Settings", "About")
        self.navbar = NavBar("Home", "Reports", "Save", "Compare")

    def _create_pages(self) -> None:
        self.pages = {}
        for P in (
            HomePage,
            ReportsPage,
            SavePage,
            ComparePage,
            AboutPage,
            SettingsPage,
        ):
            page_name = P.__name__.replace("Page", "").lower()
            page = P()
            self.pages[page_name] = page
            self.stack.addWidget(page)

    def _build_layout(self) -> None:
        # Container
        container = QWidget()
        self.setCentralWidget(container)

        # Content layout
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        content_layout.addWidget(self.navbar)
        content_layout.addWidget(self.stack)

        # Main layout
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self.topbar)
        main_layout.addLayout(content_layout)

    def _connect_signals(self) -> None:
        for page_name, page in self.pages.items():
            page.switch_page.connect(
                self.show_page
            )  # Unused, connection if pages need to switch directly.
            
            if page_name == "settings":
                page.theme_changed.connect(self.update_theme)

        self.topbar.switch_page.connect(self.show_page)
        self.navbar.switch_page.connect(self.show_page)
