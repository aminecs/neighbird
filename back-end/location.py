from geopy.geocoders import Nominatim


class GeoLocator:
    __instance = None

    @staticmethod
    def get_instance():
        """
        singleton class to get a Nominatim geolocator instance from geopy
        """
        if GeoLocator.__instance is None:
            GeoLocator.__instance = Nominatim(user_agent="codechella_dream_team")
        return GeoLocator.__instance
