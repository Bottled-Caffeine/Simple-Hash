from PyQt6.QtCore import QSettings, QSize


class Settings:
    def __init__(self) -> None:
        self._settings = QSettings()

    # Window/Size
    @property
    def remember_window_size(self) -> bool:
        return self._settings.value(
            "window/remember_size",
            False,
            type=bool,
        )

    @remember_window_size.setter
    def remember_window_size(self, value: bool) -> None:
        self._settings.setValue(
            "window/remember_size",
            value,
        )

    @property
    def window_size(self) -> QSize:
        return self._settings.value(
            "window/size",
            QSize(860, 540),
        )

    @window_size.setter
    def window_size(self, value: QSize) -> None:
        self._settings.setValue("window/size", value)

    # Interface/Theme
    @property
    def dark_theme(self) -> bool:
        return self._settings.value(
            "interface/dark_theme",
            False,
            type=bool,
        )

    @dark_theme.setter
    def dark_theme(self, value: bool) -> None:
        self._settings.setValue("interface/dark_theme", value)

    # Save/Algorithm
    @property
    def algorithm(self) -> str:
        return self._settings.value(
            "save/algorithm",
            "MD5",
            type=str,
        )

    @algorithm.setter
    def algorithm(self, value: str) -> None:
        self._settings.setValue("save/algorithm", value)

    # Save/Recursive
    @property
    def recursive(self) -> bool:
        return self._settings.value(
            "save/recursive",
            True,
            type=bool,
        )

    @recursive.setter
    def recursive(self, value: bool) -> None:
        self._settings.setValue("save/recursive", value)
