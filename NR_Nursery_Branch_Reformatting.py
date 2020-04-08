#py -3.8 -m pip install [package]

import sys
import webbrowser
import requests
import selenium
import csv
import json
import glob
import os
import time


import pandas as pd
import numpy
import numpy.core._multiarray_umath
import geopy.geocoders
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderTimedOut


from selenium import webdriver

# driver = webdriver.Chrome(r"C:\Users\Owner\Downloads\chromedriver_win32\chromedriver")
# webbrowser.open('https://docs.google.com/spreadsheets/d/1tnUy4YB6xAbic5H13RbgwL6aJF6EGUo63GgFtaVkKag/export')

# # webbrowser.open('https://docs.google.com/spreadsheets/d/1RaI3DpgY3yaIUswHbEjV9XxslLBU0reyJIQ_Gm3wA3Q/export?format=csv&id=1RaI3DpgY3yaIUswHbEjV9XxslLBU0reyJIQ_Gm3wA3Q&gid=1727268715')


time.sleep(5)

#dataframe = pd.read_csv(open('C:\\Users\\Owner\\Downloads\\Add Your Nursery (Responses) - Form Responses 1.csv', 'r'))

#dataframe = pd.read_csv(open('C:\\Users\\Owner\\Desktop\\NativesInHarmonyTest.csv', 'r'))
dataframe = pd.read_csv(open('C:\\Users\\Owner\\Downloads\\Add Your Nursery (Responses).csv', 'r'))


def geocode(df):
    
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="NR_Nursery_App")
    
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    df['location'] = df['Address (street, city)'].apply(geocode)
    #print(df['location'])
    df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else None)
    #print(df['point'])
    return df['point']


gc = geocode(dataframe)
gc = gc.apply(pd.Series, index = ['latitude', 'longitude', 'elevation'])



#Pull in the rest of the data into the dataframe in order to make futrue formatteing easier/possible.; may have to alias categorires for simplicity


# create new dataframe with geocoded lat/long + info from form
dataframe_to_convert = dataframe.join(gc)


print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

#Column rename; for future reference will have to add "Facebook" for website category
#dataframe_to_convert.columns = ['Timestamp', 'Nursery_Status', 'Nursery','State_1','Type','Native _%', 'Native', 'Keep', 'Grow_Type', 'Specialty','Address', 'Owner_Con', 'Contact_Number','Contact_Email', 'Preferred_Contact', 'Notes', 'Questions and comments', 'Zip', 'location', 'point', 'Latitude', 'Longitude', 'elevation']

dataframe_to_convert.columns = ['Timestamp', 'Nursery_Status', 'Nursery','State_1','Type','Native _%', 'Native', 'Keep', 'Grow_Type', 'Specialty','Address', 'Owner_Con', 'Contact_Number','Contact_Email', 'Preferred_Contact', 'Notes', 'Questions and comments', 'Zip', 'Facebook','location', 'point', 'Latitude', 'Longitude', 'elevation']



# convert all data to geojson
def df_to_geojson(df, properties, lat='Latitude', lon='Longitude'):
    geojson = {'type':'FeatureCollection', 'features':[]}
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

#CODE TO REMOVE NAN VALUES!!! MAKE THEM 1 OR 0 OR "FILL IN FOR NAN VALUE" SO I CAN FIND THEM EASILY OR " " WILL WORK TOO!

# for value in geojson.values:
#     if value == "nan":
#         value = " "


newFile = []


def oldFile (file):
    with open(file, 'r') as file:
        for line in file:
            sys.stdout.write(line)
            #newFile.append(line)
    return newFile

FileToModify = oldFile(r"C:\Users\Owner\Documents\Visual Studio 2017\native_nurseries_leap_ori.js") #change to full file from github




def addNewGeojson(FileToModify, geojson):

    addData = str(geojson)
    FileToModify.insert(79, addData)

    return FileToModify

ModifiedFile = addNewGeojson(FileToModify, geojson)
print (ModifiedFile)
json = json.dumps(ModifiedFile)

print("===============================================================================================================")
print (json)

with open("native_nurseries_leap.js", 'w+') as FileToUpload:
    FileToUpload.write(json)
    

""" with open("native_nurseries_leap.js", 'r') as FileToUpload:
    print(FileToUpload.read()) """







