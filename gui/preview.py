# gui/preview.py
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap
import os


class PreviewWidget(QLabel):
    file_dropped = Signal(str)

    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setText("Drag an image or video here\n\nor\n\nChoose File")

        # Keep track of the currently loaded image pixmap
        self.current_pixmap = None

        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #555555;
                border-radius: 6px;
                background-color: rgba(0, 0, 0, 0.05);
                color: #888888;
                font-size: 14px;
            }
        """)

        self.setAcceptDrops(True)

    def display_image(self, file_path: str):
        """Loads and draws an image onto the label while scaling to fit."""
        if not os.path.exists(file_path):
            self.setText("Error: File not found.")
            return

        # Load file into memory using QPixmap
        pixmap = QPixmap(file_path)

        if pixmap.isNull():
            self.setText(f"Loaded file format raw text view:\n\n{os.path.basename(file_path)}")
            self.current_pixmap = None
            return

        # Store layout parameters and strip text borders for clean media presentation
        self.current_pixmap = pixmap
        self.setStyleSheet("QLabel { background-color: rgba(0, 0, 0, 0.1); border: none; }")
        self.update_preview()

    def update_preview(self):
        """Rescales the image to match the container's active geometry dimensions."""
        if self.current_pixmap:
            # Scale dynamically preserving height-to-width proportions smoothly
            scaled_pixmap = self.current_pixmap.scaled(
                self.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.setPixmap(scaled_pixmap)

    def resizeEvent(self, event):
        """Triggered automatically by Qt when the user resizes the window or splitter."""
        super().resizeEvent(event)
        if self.current_pixmap:
            self.update_preview()

    # --- Keep existing Drag and Drop methods intact ---
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet("QLabel { border: 2px dashed #3498db; background-color: rgba(52, 152, 219, 0.1); }")

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        if not self.current_pixmap:
            self.reset_ui_style()

    def dropEvent(self, event):
        if not self.current_pixmap:
            self.reset_ui_style()
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if file_path:
                self.file_dropped.emit(file_path)

    def reset_ui_style(self):
        self.setStyleSheet(
            "QLabel { border: 2px dashed #555555; border-radius: 6px; background-color: rgba(0, 0, 0, 0.05); color: #888888; }")