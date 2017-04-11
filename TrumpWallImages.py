# https://maps.googleapis.com/maps/api/streetview?size=1200x800&location=32.731841,-117.04834&key=AIzaSyAkplPDKwEuD63K2NGrXKnDq4PmVRKq0x0
# https://maps.googleapis.com/maps/api/staticmap?center=40.714728,-73.998672&zoom=12&size=400x400&maptype=satellite&key=YOUR_API_KEY

import urllib.request
import requests
import json

from threading import Timer
import time
from secrets import *
from random import randint
from random import uniform


#First longitude coordinate
initialLon = -117.04834 + 0.01

currLon = -117.04834 + 0.01

#will hold the data for the current iteration
data = []

def getCoordinates(num):
    section = randint(0,4)
    lat = 0.0
    lon = 0.0

    global currLon

    lat = 32.731841
    currLon = initialLon + (float(num)*0.01)



    if(currLon > -97.0) {
        raise Exception("Reached the end of the border")
    }

    latLon = [lat, currLon]
    # print(latLon)
    return latLon

def getImages(lat, lon, num):
    global data
    satelliteAPIKey = "AIzaSyCPkf-opRHSnbRMJXdhcTYI3cnurj6ac5g"
    linkPt1 = "https://maps.googleapis.com/maps/api/staticmap?center="
    linkStr = linkPt1 + str(lat) + "," + str(lon) + "&zoom=20&size=400x400&maptype=satellite&key=" + satelliteAPIKey
    # print(linkStr)
    name = "pics/satellite/" + str(num) + ".jpg"
    print("saving satellite to " + name)
    urllib.request.urlretrieve(linkStr, name)
    data[1].append({"name": name, "location": [lat, lon]})

    linkStr = linkPt1 + str(lat) + "," + str(lon) + "&zoom=20&size=400x400&maptype=roadmap&key=" + satelliteAPIKey
    # print(linkStr)
    name = "pics/map/" + str(num) + ".jpg"
    urllib.request.urlretrieve(linkStr, name)
    print("saving map to " + name)
    data[0].append({"name": name, "location": [lat, lon]})

    linkPt1 = "https://maps.googleapis.com/maps/api/streetview?size=1200x800&location="
    linkStr = linkPt1 + str(lat) + "," + str(lon) + "&radius=50&key=AIzaSyAkplPDKwEuD63K2NGrXKnDq4PmVRKq0x0"
    # print(linkStr)
    name = "pics/street/" + str(num) + ".jpg"
    urllib.request.urlretrieve(linkStr, name)
    print("saving street to " + name)
    data[2].append({"name": name, "location": [lat, lon]})
    # return linkStr




def setInterval(func, sec):
    def func_wrapper():
        setInterval(func, sec)
        func()
    t = Timer(sec, func_wrapper)
    t.start()
    return t


def runBot():

    #see how many images are already in the json
    #so that we know from where to continue on the border
    counter = 0   
    with open('data.json', 'r') as f:
        json_data = json.load(f)
        counter = len(json_data["map"])
        f.close()


    #clear out the data from last iteration
    global data  
    del data[:]
    for i in range(0,3):
        data.append([])

    r = 50 #the range for this run (how many pictures to get)

    #get images within the range
    try:
        for i in range(0, r):
            print("iteration " + str(i))
        
            latLon = getCoordinates(i + counter)
            getImages(latLon[0], latLon[1], i + counter)
    except Exception as err:
        print(err)

    if(currLon > -97.0) {
        raise Exception("Process is finished.")
    }

    #append to the current data
    json_data["map"] = json_data["map"] + data[0]
    json_data["satellite"] = json_data["satellite"] + data[1]
    json_data["street"] = json_data["street"] + data[2]

    #write to json file
    with open('data.json', 'w') as f:
        json.dump(json_data,f)

        f.close()

    # createMeme(imageLink)



debug = False
runOnce = False

runBot()
if not runOnce:
    setInterval(runBot, 60*60)  #runs every hour