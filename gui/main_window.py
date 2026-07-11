from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QStatusBar,
)

from gui.preview import PreviewWidget
from gui.metadata_tabs import MetadataTabs
from gui.toolbar import ToolBar
from gui.menu_bar import MenuBar


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("MetaLens")
        self.resize(1400, 850)

        self.setup_ui()

    def setup_ui(self):

        # Toolbar
        self.addToolBar(ToolBar())
        self.setMenuBar(
            MenuBar(self)
        )

        # Central Widget
        central = QWidget()

        layout = QHBoxLayout()

        layout.addWidget(PreviewWidget(), 2)
        layout.addWidget(MetadataTabs(), 3)

        central.setLayout(layout)

        self.setCentralWidget(central)

        self.setStatusBar(QStatusBar())