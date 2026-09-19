from PyQt6.QtWidgets import QTextBrowser, QWidget

from simple_hash.services import resource_path


class MarkdownViewer(QTextBrowser):
    def __init__(
        self,
        path: str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.setReadOnly(True)

        with open(resource_path(path), "r", encoding="utf-8") as f:
            self.setMarkdown(f.read())
