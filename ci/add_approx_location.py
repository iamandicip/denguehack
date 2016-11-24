import pandas as pd
import csv
from geopy.geocoders import Nominatim

csv_file_path = 'tweets_south_america.csv'

df = pd.read_csv(csv_file_path, header=0, sep=',', parse_dates=[1], quoting=csv.QUOTE_ALL, encoding='utf-8')
df.set_index(['id'])


df['approx_lat'] = pd.Series(df['geo'])
df['approx_long'] = pd.Series(df['geo'])

# print(df.head())

geolocator = Nominatim()

def get_locations(geos):
    locations = {}
    for geo in geos:
        print(geo)
        location = geolocator.geocode(geo)
        locations[geo] = (location.latitude, location.longitude)
    print(len(locations))
    return locations

unique_locs = df['geo'].unique()
unique_approx = get_locations(unique_locs)

def get_approx_lat(geo):
    return unique_approx[geo][0]

def get_approx_long(geo):
    return unique_approx[geo][1]

df['approx_lat'].map(lambda geo : get_approx_lat(geo))
df['approx_long'].map(lambda geo : get_approx_long(geo))

df.to_csv('tweets_south_america_approx.csv')
