# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 21:04:52 2016

@author: koopac

Call this as 'python3 jsont2csv.py tweetFile.json'
It will extract time and location info from the json file

"""
import sys
import json
import statistics as stat
import csv
from os.path import splitext

myFile=open(sys.argv[1], mode='rt')

# Each line is a json object
myJs=[ json.loads(line) for line in myFile ]

# needed fields: "created_at", "id_str", "geo",
# place"/
#        "country_code"
#        "name"
#        "bounding box"/
#                       "coordinates"
myData=[ [jso['id_str'], jso['created_at'], jso['geo'],
          jso['place']['country'], jso['place']['country_code'],
          jso['place']['name'], jso['place']['bounding_box']['coordinates']] 
          for jso in myJs ]

# Exact coordinates (where available)
xLats=[]
xLons=[]
for i in range(len(myData)):
    try: xLats.append(myData[i][2]['coordinates'][0])
    except TypeError:
        xLats.append('')
    try: xLons.append(myData[i][2]['coordinates'][1])
    except TypeError:
        xLons.append('')


# Average bounding box coordinates (latitudes and longitudes)
lats=[ stat.mean([ x[0] for x in entry[6][0] ])  for entry in myData]
lons=[ stat.mean([ y[1] for y in entry[6][0] ])  for entry in myData]

# Prepare data to export to csv
finalData=[['id', 'date', 'lat', 'lon', 'country', 'countryCode', 'place',
            'approxLat', 'approxLon']]
for i in range(len(myData)):
    finalData.append(myData[i][0:2])
    finalData[i+1].append(xLats[i])
    finalData[i+1].append(xLons[i])
    finalData[i+1]=finalData[i+1]+myData[i][3:6]
    finalData[i+1].append(lats[i])
    finalData[i+1].append(lons[i])

# Write to file (same name as json)
csvFile=open(splitext(sys.argv[1])[0]+'.csv', mode='wt')
wr=csv.writer(csvFile)
wr.writerows(finalData)
