from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenuBar


class MenuBar(QMenuBar):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.create_file_menu()
        self.create_view_menu()
        self.create_tools_menu()
        self.create_help_menu()

    def create_file_menu(self):

        file_menu = self.addMenu("File")

        open_action = QAction("Open File...", self)
        export_action = QAction("Export Metadata", self)
        compare_action = QAction("Compare Files", self)
        exit_action = QAction("Exit", self)

        file_menu.addAction(open_action)
        file_menu.addAction(export_action)
        file_menu.addAction(compare_action)

        file_menu.addSeparator()

        file_menu.addAction(exit_action)


    def create_view_menu(self):

        view_menu = self.addMenu("View")

        toolbar_action = QAction(
            "Show Toolbar",
            self
        )

        status_action = QAction(
            "Show Status Bar",
            self
        )

        dark_action = QAction(
            "Toggle Dark Mode",
            self
        )

        view_menu.addAction(toolbar_action)
        view_menu.addAction(status_action)
        view_menu.addAction(dark_action)


    def create_tools_menu(self):

        tools_menu = self.addMenu("Tools")

        clean_action = QAction(
            "Remove Metadata",
            self
        )

        settings_action = QAction(
            "Settings",
            self
        )

        tools_menu.addAction(clean_action)
        tools_menu.addAction(settings_action)


    def create_help_menu(self):

        help_menu = self.addMenu("Help")

        about_action = QAction(
            "About MetaLens",
            self
        )

        help_menu.addAction(about_action)