# services/metadata.py
import exiftool
import os
from services.geocoder import GeocoderService


class MetadataService:
    def __init__(self):
        self.geocoder = GeocoderService()
        pass

    def extract_metadata(self, file_path: str) -> dict:
        """
        Reads a file and returns a organized dictionary partitioned by category.
        """
        if not os.path.exists(file_path):
            return {"error": "File does not exist."}

        try:
            with exiftool.ExifToolHelper() as et:
                # et.get_metadata returns a list containing a dict of tags
                metadata_list = et.get_metadata(file_path)
                if not metadata_list:
                    return {"error": "No metadata could be extracted."}

                raw_tags = metadata_list[0]
                return self._categorize_tags(raw_tags, file_path)
        except Exception as e:
            return {"error": f"ExifTool extraction failed: {str(e)}"}

    def _categorize_tags(self, raw: dict, file_path: str) -> dict:
        """
        Sorts raw flat tags into semantic buckets for our UI tabs.
        """
        categories = {
            "General": {},
            "Camera": {},
            "GPS": {},
            "Dates": {},
            "Technical": {},
            "Raw": {}
        }

        # Inject basic filesystem parameters manually into General
        categories["General"]["File Name"] = os.path.basename(file_path)
        categories["General"]["File Size"] = f"{os.path.getsize(file_path) / 1024:.2f} KB"

        for tag, value in raw.items():
            # Clean up the tag naming convention (e.g., 'EXIF:Model' -> 'Model')
            clean_tag = tag.split(":")[-1] if ":" in tag else tag

            # Populate Raw tab completely with everything
            categories["Raw"][tag] = str(value)

            # Route tags to specific display buckets based on ExifTool prefix groups
            if tag.startswith("EXIF:") or tag.startswith("MakerNotes:"):
                if "Date" in clean_tag or "Time" in clean_tag:
                    categories["Dates"][clean_tag] = str(value)
                elif "GPS" in tag:
                    categories["GPS"][clean_tag] = str(value)
                elif clean_tag in ["Make", "Model", "LensModel", "SerialNumber", "LensInfo"]:
                    categories["Camera"][clean_tag] = str(value)
                else:
                    categories["Technical"][clean_tag] = str(value)

            elif tag.startswith("Composite:"):
                if "GPS" in clean_tag:
                    categories["GPS"][clean_tag] = str(value)
                else:
                    categories["Technical"][clean_tag] = str(value)

            elif tag.startswith("XMP:") or tag.startswith("IPTC:"):
                if "Date" in clean_tag:
                    categories["Dates"][clean_tag] = str(value)
                else:
                    categories["General"][clean_tag] = str(value)

            elif tag.startswith("File:"):
                if clean_tag not in ["FileName", "FileSize"]:
                    categories["General"][clean_tag] = str(value)

        return categories