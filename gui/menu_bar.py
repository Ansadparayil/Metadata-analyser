# gui/menu_bar.py
from PySide6.QtWidgets import QMenuBar
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtCore import Signal


class MenuBar(QMenuBar):
    # Signals to communicate intent cleanly out to the MainWindow controller
    open_requested = Signal()
    export_requested = Signal()
    clean_requested = Signal()
    exit_requested = Signal()
    toggle_toolbar_requested = Signal(bool)
    toggle_dark_mode_requested = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_menus()

    def _init_menus(self):
        # File Menu
        file_menu = self.addMenu("&File")

        open_act = QAction("&Open File...", self)
        open_act.setShortcut(QKeySequence.Open)
        open_act.triggered.connect(self.open_requested.emit)
        file_menu.addAction(open_act)

        export_act = QAction("&Export...", self)
        export_act.setShortcut(QKeySequence.Save)
        export_act.triggered.connect(self.export_requested.emit)
        file_menu.addAction(export_act)

        file_menu.addSeparator()

        exit_act = QAction("E&xit", self)
        exit_act.triggered.connect(self.exit_requested.emit)
        file_menu.addAction(exit_act)

        # View Menu
        view_menu = self.addMenu("&View")

        toggle_tb_act = QAction("Show &Toolbar", self, checkable=True)
        toggle_tb_act.setChecked(True)
        toggle_tb_act.triggered.connect(self.toggle_toolbar_requested.emit)
        view_menu.addAction(toggle_tb_act)

        dark_act = QAction("Dark &Theme", self, checkable=True)
        dark_act.triggered.connect(self.toggle_dark_mode_requested.emit)
        view_menu.addAction(dark_act)

        # Tools Menu
        tools_menu = self.addMenu("&Tools")

        clean_act = QAction("&Clean Metadata", self)
        clean_act.triggered.connect(self.clean_requested.emit)
        tools_menu.addAction(clean_act)
