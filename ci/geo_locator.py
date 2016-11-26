
from geopy.geocoders import Nominatim
from geopy.geocoders import GeoNames

class GeoLocator:

    def get_coordinates_for_location(self, location_name):
        result = None

        # geolocator = Nominatim()
        geolocator = GeoNames(timeout=10, username='iamandicip')
        location = geolocator.geocode(location_name, exactly_one=True)

        # print(dir(location))

        if location and location.latitude and location.longitude:
            result = (location.latitude, location.longitude)
        else:
            print('No coordinates found for location: {0}'.format(location_name))

        return result

if __name__ == '__main__':
    gl = GeoLocator()
    gl.get_coordinates_for_location('Alta Floresta, Brazil')
