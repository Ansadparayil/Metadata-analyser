# gui/main_window.py
from PySide6.QtWidgets import QMainWindow, QSplitter, QStatusBar
from PySide6.QtCore import Slot, Qt

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
        # 1. Instantiate Actions / Bars
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)

        self.toolbar = ToolBar()
        self.addToolBar(self.toolbar)

        # 2. Core Dynamic Layout: Using QSplitter instead of simple QHBoxLayout
        # This addresses Phase 1.5 UI Polish goals perfectly
        self.splitter = QSplitter(Qt.Horizontal)

        self.preview_widget = PreviewWidget()
        self.metadata_tabs = MetadataTabs()

        self.splitter.addWidget(self.preview_widget)
        self.splitter.addWidget(self.metadata_tabs)

        # Maintain your 2:3 layout proportions through stretch factor allocation
        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 3)

        self.setCentralWidget(self.splitter)

        # 3. Status Bar Tracking
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Ready")

        # 4. Bind Actions
        self._connect_signals()

    def _connect_signals(self):
        # Connect Menu Actions
        self.menu_bar.open_requested.connect(self.handle_open_file)
        self.menu_bar.export_requested.connect(self.handle_export)
        self.menu_bar.clean_requested.connect(self.handle_clean_metadata)
        self.menu_bar.exit_requested.connect(self.close)
        self.menu_bar.toggle_toolbar_requested.connect(self.handle_toggle_toolbar)
        self.menu_bar.toggle_dark_mode_requested.connect(self.handle_toggle_dark_mode)

    @Slot()
    def handle_open_file(self):
        self.status.showMessage("Opening file browser...")

    @Slot()
    def handle_export(self):
        self.status.showMessage("Exporting metadata report...")

    @Slot()
    def handle_clean_metadata(self):
        self.status.showMessage("Cleaning tracking artifacts...")

    @Slot(bool)
    def handle_toggle_toolbar(self, visible: bool):
        self.toolbar.setVisible(visible)

    @Slot(bool)
    def handle_toggle_dark_mode(self, enabled: bool):
        self.status.showMessage(f"Dark Theme Set: {enabled}")