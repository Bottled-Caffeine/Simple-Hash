from PyQt6.QtCore import QByteArray, QSize, Qt
from PyQt6.QtGui import QColor, QFont, QIcon, QPainter, QPalette, QPixmap
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QApplication

from simple_hash.services import resource_path
from simple_hash.settings import Settings

from .constants import FONT, STYLES_ICONS


def load_style(app: QApplication) -> None:
    settings = Settings()

    app.setFont(QFont(FONT["name"], FONT["size"]))

    _set_palette(app, settings)

    style = (
        "assets/styles/base.qss"
        if not settings.dark_theme
        else "assets/styles/dark.qss"
    )

    with open(resource_path(style), "r", encoding="utf-8") as f:
        style = _edit_style(f.read())
        app.setStyleSheet(style)


def load_icon(path: str) -> QIcon:
    settings = Settings()
    path = resource_path(path)

    color = "black" if not settings.dark_theme else "white"

    svg = path.read_text(encoding="utf-8")
    svg = svg.replace("currentColor", color)

    renderer = QSvgRenderer(QByteArray(svg.encode()))

    pixmap = QPixmap(QSize(128, 128))
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()

    return QIcon(pixmap)


def _set_palette(app: QApplication, settings: Settings) -> None:

    color = "#e6e8eB" if settings.dark_theme else "#333333"

    palette = app.palette()
    palette.setColor(QPalette.ColorRole.WindowText, QColor(color))
    palette.setColor(QPalette.ColorRole.Text, QColor(color))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(color))
    palette.setColor(
        QPalette.ColorRole.Highlight,
        QColor(color),
    )

    app.setPalette(palette)


def _edit_style(style: str) -> str:

    for key, value in STYLES_ICONS.items():
        style = style.replace(key, resource_path(value).as_posix())

    return style
