# services/geocoder.py
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import re


class GeocoderService:
    def __init__(self):
        # Initialize Nominatim Geocoder with an identifying user agent string
        self.geolocator = Nominatim(user_agent="metalens_forensic_analyzer")

    def parse_dms_to_decimal(self, coordinate_str: str) -> float:
        """
        Helper method to parse Degrees/Minutes/Seconds or text strings into floats.
        Example: '51 deg 30\' 26.00" N' -> 51.5072
        """
        if not coordinate_str:
            return 0.0

        # If it's already a clean float string, return it directly
        try:
            return float(coordinate_str)
        except ValueError:
            pass

        # Extract numeric components via regex matching numbers/decimals
        numbers = re.findall(r"[-+]?\d*\.\d+|\d+", coordinate_str)
        if not numbers:
            return 0.0

        # Extract degrees, minutes, seconds based on what's available
        deg = float(numbers[0]) if len(numbers) > 0 else 0.0
        mn = float(numbers[1]) if len(numbers) > 1 else 0.0
        sec = float(numbers[2]) if len(numbers) > 2 else 0.0

        decimal = deg + (mn / 60.0) + (sec / 3600.0)

        # Check for Southern or Western hemisphere notations to flip the sign
        if any(direction in coordinate_str.upper() for direction in ['S', 'W']) or deg < 0:
            decimal = -abs(decimal)

        return decimal

    def get_address(self, latitude_raw: str, longitude_raw: str) -> dict:
        """
        Converts raw coordinates into a decimal pair and retrieves a human address.
        """
        try:
            lat = self.parse_dms_to_decimal(str(latitude_raw))
            lon = self.parse_dms_to_decimal(str(longitude_raw))

            if lat == 0.0 and lon == 0.0:
                return {"error": "Invalid or missing coordinates."}

            # Perform lookup request
            location = self.geolocator.reverse((lat, lon), timeout=4)

            if location:
                return {
                    "latitude": lat,
                    "longitude": lon,
                    "address": location.address,
                    "details": location.raw.get("address", {})
                }
            return {"latitude": lat, "longitude": lon, "address": "Coordinates identified but no address resolved."}

        except (GeocoderTimedOut, GeocoderServiceError) as e:
            return {"latitude": lat, "longitude": lon, "address": f"Geocoding service unavailable: {str(e)}"}
        except Exception as e:
            return {"error": f"Resolution failed: {str(e)}"}