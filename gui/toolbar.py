from PySide6.QtGui import QAction
from PySide6.QtWidgets import QToolBar


class ToolBar(QToolBar):

    def __init__(self):
        super().__init__("Main Toolbar")

        open_action = QAction("Open", self)
        export_action = QAction("Export", self)
        clean_action = QAction("Clean Metadata", self)

        self.addAction(open_action)
        self.addSeparator()
        self.addAction(export_action)
        self.addAction(clean_action)