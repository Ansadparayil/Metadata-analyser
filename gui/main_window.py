# gui/main_window.py
from PySide6.QtWidgets import QMainWindow, QSplitter, QStatusBar, QFileDialog # Added QFileDialog
from PySide6.QtCore import Slot, Qt
import os

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
        self.preview_widget.file_dropped.connect(self.load_file)

    @Slot()
    def handle_open_file(self):
        self.status.showMessage("Opening file browser...")

        # Open standard file selector supporting standard image and video extensions
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Media File",
            "",
            "Media Files (*.jpg *.jpeg *.png *.heic *.mp4 *.mov *.avi);;All Files (*.*)"
        )

        if file_path:
            self.load_file(file_path)

    @Slot(str)
    def load_file(self, file_path: str):
        """
        Entry point for handling loaded files via either Drag & Drop or File Browser.
        """
        filename=os.path.basename(file_path)
        self.status.showMessage(f"Loading file: {file_path}")

        # Temporary visual feedback to confirm it works:
        self.preview_widget.display_image(file_path)

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