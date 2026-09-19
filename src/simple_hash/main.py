from PyQt6.QtCore import QCoreApplication, QSettings
from PyQt6.QtWidgets import QApplication

from simple_hash.ui.styles import load_style
from simple_hash.ui.windows import MainWindow
from simple_hash.version import __version__


def main() -> None:
    QCoreApplication.setOrganizationName("SimpleHash")
    QCoreApplication.setApplicationName("SimpleHash")
    QCoreApplication.setApplicationVersion(__version__)

    QSettings.setDefaultFormat(QSettings.Format.IniFormat)

    app = QApplication([])

    load_style(app)

    window = MainWindow()

    window.show()
    app.exec()


if __name__ == "__main__":
    main()
