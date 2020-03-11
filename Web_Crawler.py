#py -3.8 -m pip install [package]

import webbrowser
import requests
import selenium
import csv
import json
import glob
import os
import time
import geopandas
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderTimedOut
import fileinput


from selenium import webdriver

#driver = webdriver.Chrome()
#webbrowser.open('https://docs.google.com/spreadsheets/d/1RaI3DpgY3yaIUswHbEjV9XxslLBU0reyJIQ_Gm3wA3Q/export?format=csv&id=1RaI3DpgY3yaIUswHbEjV9XxslLBU0reyJIQ_Gm3wA3Q&gid=1727268715')
#driver.implicitly_wait(3)

#time.sleep(5)

dataframe = pd.read_csv(open('C:\\Users\\itj\\Downloads\\Add Your Nursery (Responses) - Form Responses 1.csv', 'r'))

#jsfile = ("this is a test js file. \n For use with the concatenate function\n This is also a test.\n This too")


def geocode(df):

    
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="NR_Nursery_App")
    
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    df['location'] = df['Address (street, city)'].apply(geocode)
    print(df['location'])
    df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else None)
    print(df['point'])
    return df['point']



gc = geocode(dataframe)
gc = gc.apply(pd.Series, index = ['latitude', 'longitude', 'elevation'])



# create new dataframe with geocoded lat/long + info from form
dataframe_to_convert = dataframe.join(gc)


# convert all data to geojson
def df_to_geojson(df, properties, lat='latitude', lon='longitude'):
    geojson = {'type':'FeatureCollection', 'features':[]} #May need to change desginations and {} for production version
    for _, row in df.iterrows():
        feature = {'type':'Feature',
                   'properties':{},
                   'geometry':{'type':'Point',
                               'coordinates':[]}}
        feature['geometry']['coordinates'] = [row[lon],row[lat]]
        for prop in properties:
            feature['properties'][prop] = row[prop]
        geojson['features'].append(feature)
    return geojson

cols = list(dataframe_to_convert)
geojson = df_to_geojson(dataframe_to_convert, cols)
#print(geojson)



def concatenate (file, geojson):
    with open(file, 'r+') as jsfile:
        lines = jsfile.readlines()
        addData = "\n{" + str(geojson) + ",\n"
        lines.insert(68, addData) #This number will be 79 in the production version
        return lines        
    #print (lines)





a = concatenate(r"C:\Users\itj\Desktop\Visual_Studio_Code\NR_Nurseries\Nursery_Concatenate_Test.txt", geojson)
#print(a)


geojsonString = ''.join(a)
#print(geojsonString) # This is just the lines not the file itself I think?
#Should I pull the data modify it and then stick it back in the file or modify the file directly?

print (json.dumps(geojsonString))


#how do i automatically put this geojson in github?
#how to I auto format it to fit the format (labels, true/false) of the current data files?
#can i alias the column names?Then what about true/false designations, the single v double quotes?
#how do I add the relevent data to both files, nurseries.js and native_nurseries_leap.js?
#how do I integrate the nursery data onto the website, seed, plants, clonal, etc.?

#Must delete file after running as it will always choose the first one downloaded
