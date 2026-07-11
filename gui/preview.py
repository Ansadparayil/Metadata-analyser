from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel


class PreviewWidget(QLabel):

    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignCenter)

        self.setText(
            "Drag an image or video here\n\nor\n\nChoose File"
        )