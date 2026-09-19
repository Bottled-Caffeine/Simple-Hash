from PyQt6.QtWidgets import QMessageBox, QWidget


class DeleteMessage(QMessageBox):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.setIcon(QMessageBox.Icon.Warning)
        self.setWindowTitle("Confirm Deletion")
        self.setText("The selected reports will be permanently deleted.\nContinue?")

        self.continue_button = self.addButton(
            "Continue", QMessageBox.ButtonRole.AcceptRole
        )
        self.cancel_button = self.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
