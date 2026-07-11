# gui/preview.py
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QLabel


class PreviewWidget(QLabel):
    # Custom signal to notify MainWindow when a valid file is dropped
    file_dropped = Signal(str)

    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setText("Drag an image or video here\n\nor\n\nChoose File")

        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #555555;
                border-radius: 6px;
                background-color: rgba(0, 0, 0, 0.05);
                color: #888888;
                font-size: 14px;
            }
        """)

        # Enable drop events on this widget
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        # Check if the drag payload contains local URLs (files)
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet("""
                QLabel {
                    border: 2px dashed #3498db;
                    border-radius: 6px;
                    background-color: rgba(52, 152, 219, 0.1);
                    color: #3498db;
                    font-size: 14px;
                }
            """)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        # Reset stylesheet if the user drags out of the widget without dropping
        self.reset_ui_style()

    def dropEvent(self, event):
        self.reset_ui_style()
        urls = event.mimeData().urls()

        if urls:
            # Grab the first file path dropped
            file_path = urls[0].toLocalFile()
            if file_path:
                # Emit the path upwards to MainWindow
                self.file_dropped.emit(file_path)

    def reset_ui_style(self):
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #555555;
                border-radius: 6px;
                background-color: rgba(0, 0, 0, 0.05);
                color: #888888;
                font-size: 14px;
            }
        """)