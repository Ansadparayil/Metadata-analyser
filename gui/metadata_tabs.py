# gui/metadata_tabs.py
from PySide6.QtWidgets import QTabWidget, QTextEdit


class MetadataTabs(QTabWidget):
    def __init__(self):
        super().__init__()

        # Track individual text areas mapping strictly to our service keys
        self.tab_editors = {}

        self.tabs_list = [
            "General",
            "Camera",
            "GPS",
            "Dates",
            "Technical",
            "Raw"
        ]

        for tab_name in self.tabs_list:
            text_area = QTextEdit()
            text_area.setReadOnly(True)
            # Apply a clean mono font style presentation for readable rows
            text_area.setStyleSheet("font-family: 'Courier New', monospace; font-size: 13px; padding: 10px;")

            self.addTab(text_area, tab_name)
            self.tab_editors[tab_name] = text_area

    def display_metadata(self, structured_data: dict):
        """
        Receives categorized metadata and fills the appropriate text windows.
        """
        # Clear out any stale text displays first
        self.clear_all_tabs()

        if "error" in structured_data:
            self.tab_editors["General"].setText(f"Error analyzing file:\n{structured_data['error']}")
            return

        for category, tags in structured_data.items():
            if category in self.tab_editors:
                # Format block contents cleanly: "Tag Name : Value"
                content_lines = []
                for tag, val in sorted(tags.items()):
                    content_lines.append(f"{tag:<30}: {val}")

                display_text = "\n".join(content_lines) if content_lines else "No records found under this group."
                self.tab_editors[category].setText(display_text)

    def clear_all_tabs(self):
        for text_area in self.tab_editors.values():
            text_area.clear()