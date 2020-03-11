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
import geopy.geocoders
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderTimedOut


from selenium import webdriver

#driver = webdriver.Chrome()
#webbrowser.open('https://docs.google.com/spreadsheets/d/1RaI3DpgY3yaIUswHbEjV9XxslLBU0reyJIQ_Gm3wA3Q/export?format=csv&id=1RaI3DpgY3yaIUswHbEjV9XxslLBU0reyJIQ_Gm3wA3Q&gid=1727268715')
#driver.implicitly_wait(3)1`

#time.sleep(5)

dataframe = pd.read_csv(open('C:\\Users\\itj\\Downloads\\Add Your Nursery (Responses) - Form Responses 1.csv', 'r'))



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
#print(dataframe_to_convert["location"])

# convert all data to geojson
def df_to_geojson(df, properties, lat='latitude', lon='longitude'):
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
#print(geojson)

newFile = []


def oldFile (file):
    with open(file, 'r') as file:
        for line in file:
            sys.stdout.write(line)
            #newFile.append(line)
    return newFile


print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")


FileToModify = oldFile(r"C:\Users\itj\Desktop\Visual_Studio_Code\NR_Nurseries\native_nurseries_leap_ori.js") #change to full file from github

print(FileToModify)
""" 
print(len(FileToModify)) """


""" print(type(FileToModify))
print(FileToModify)
print(FileToModify[2])
print(type(FileToModify[2])) """

""" 
print ('========================================================================================================')
jsonDumps = json.dumps(FileToModify)
print (jsonDumps)
print (type(jsonDumps)) """


def addNewGeojson(FileToModify, geojson):

    #addData = "\n{" + str(geojson) + ",\n"
    #addData = "\n{" + str(geojson) + "}\n},\n"
    addData = str(geojson)
    FileToModify.insert(79, addData) #change to 79

    return FileToModify

ModifiedFile = addNewGeojson(FileToModify, geojson)
#print(type(ModifiedFile))
#print (len(ModifiedFile))


#print(ModifiedFile[67])
#print(type(ModifiedFile[67]))
json = json.dumps(ModifiedFile)
#json = json.dumps(ModifiedFile[67])
print("===============================================================================================================")
print (json)
print("===============================================================================================================")


with open("native_nurseries_leap.js", 'w+') as FileToUpload:
    FileToUpload.write(json)
    

""" with open("native_nurseries_leap.js", 'r') as FileToUpload:
    print(FileToUpload.read()) """



#print(json, file=open("native_nurseries_leap.js", "w"))


""" with open("native_nurseries_leap.js", 'r') as FileToUpload:
    read = FileToUpload.read()
    print (read) """



# file1 = open("native_nurseries_leap.js")
# print (file1.read())

""" 
print(len(file1.read())) """
#Do I ultimately need a dictionary? I think I can use json.dumps()

#Need to figure out how to prevent endless addition?

#how do i automatically put this geojson in github?
#how to I auto format it to fit the format (labels, true/false) of the current data files?
#can i alias the column names?Then what about true/false designations, the single v double quotes?
#how do I add the relevent data to both files, nurseries.js and native_nurseries_leap.js?
#how do I integrate the nursery data onto the website, seed, plants, clonal, etc.?

#Must delete file after running as it will always choose the first one downloaded

