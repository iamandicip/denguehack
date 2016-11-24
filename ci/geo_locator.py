
from geopy.geocoders import Nominatim

class GeoLocator:

    def get_coordinates_for_location(self, location):
        geolocator = Nominatim()
        location = geolocator.geocode(location)
        return location.latitude, location.longitude
