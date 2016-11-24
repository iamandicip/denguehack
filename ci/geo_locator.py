
from geopy.geocoders import Nominatim

class GeoLocator:

    def get_coordinates_for_location(self, location_name):
        result = None

        geolocator = Nominatim()
        location = geolocator.geocode(location_name)
        
        if location is None or location.latitude is None or location.longitude is None:
            print('No coordinates found for location: {0}'.format(location_name))
        else:
            result = (location.latitude, location.longitude)

        return result
