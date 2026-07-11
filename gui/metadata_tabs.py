from PySide6.QtWidgets import QTabWidget, QTextEdit


class MetadataTabs(QTabWidget):

    def __init__(self):
        super().__init__()

        tabs = [
            "General",
            "Camera",
            "GPS",
            "Dates",
            "Technical",
            "Raw"
        ]

        for tab in tabs:
            text = QTextEdit()
            text.setReadOnly(True)
            self.addTab(text, tab)