import json

import os

import time

from scripts.enrich.clean import clean
from scripts.enrich.weather import augmentWeather
from scripts.enrich.sentiment import sentiment
from scripts.utils import utils


def countAllPlaces():
    with open(utils.getFullPathFromDataFileName('places.json')) as data_file:
        places = json.load(data_file)

        placeCounts = []
        for place in places:
            cityName = place["name"]
            cityProperName = place["properName"]


            if cityDataExists(cityName):
                placeCounts.append((cityProperName, countData(cityName)))
            else:
                print 'No data file found for: ', cityProperName
        placeCountsSorted = sorted(((v, k) for k, v in placeCounts), reverse=True)
        for key, value in placeCountsSorted:
            print value + ': ' + str(key)

def countData(cityName):
    inputPath = utils.getFullPathFromDataFileName(cityName + '.json')
    with open(inputPath) as data_file:
        dataEntries = json.load(data_file)
        return len(dataEntries)

def cityDataExists(cityName):
    cityFileName = cityName + '.json'
    cityFilePath = utils.getFullPathFromDataFileName(cityFileName)
    return os.path.isfile(cityFilePath)


countAllPlaces()
