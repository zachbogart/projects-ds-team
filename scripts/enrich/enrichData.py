import json

import os

import time

from scripts.enrich.clean import clean
from scripts.enrich.weather import augmentWeather
from scripts.enrich.sentiment import sentiment
from scripts.utils import utils


def enrichAllPlaces():
    global cityName
    with open(utils.getFullPathFromDataFileName('places.json')) as data_file:
        places = json.load(data_file)

        for place in places:
            cityName = place["name"]
            cityProperName = place["properName"]
            coordinates = place["coordinates"]

            print ''
            print ''
            print 'About to enrich: ', cityProperName
            if cityDataExists(cityName):
                print 'City Data found for: ', cityProperName

                # Enrich with weather data
                print 'Enriching with Weather Data'
                augmentWeather.enrichWithWeather(cityName, coordinates)

                # Enrich with sentiment
                print 'Enriching with Sentiment'
                sentiment.enrichWithSentiment(cityName)

                # Clean data
                print 'Cleaning Data'
                clean.clean(cityName)
            else:
                print 'No data file found for: ', cityProperName


def cityDataExists(cityName):
    cityFileName = cityName + '.json'
    cityFilePath = utils.getFullPathFromDataFileName(cityFileName)
    return os.path.isfile(cityFilePath)


enrichAllPlaces()
