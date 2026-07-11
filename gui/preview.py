# gui/preview.py
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel


class PreviewWidget(QLabel):

    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setText("Drag an image or video here\n\nor\n\nChoose File")

        # UI polish: give it a distinct layout boundary look
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #555555;
                border-radius: 6px;
                background-color: rgba(0, 0, 0, 0.05);
                color: #888888;
                font-size: 14px;
            }
        """)

        # Prepping for next phase item
        self.setAcceptDrops(True)