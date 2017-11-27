import json

import os

from scripts.enrich.clean import clean
from scripts.enrich.weather import augmentWeather
from scripts.enrich.sentiment import sentiment
from scripts.utils import utils


def enrichAllPlaces():
    global cityName
    with open(utils.getFullPathFromDataFileName('places.json')) as data_file:
        places = json.load(data_file)

        for place in places():
            # Get twitter data for city
            cityName = place["name"]
            cityProperName = place["properName"]
            cityBoundingBox = place["boundingBox"]
            cityWeatherStationID = place["weatherStationID"]

            if cityDataExists():
                # Enrich with weather data
                augmentWeather.enrichWithWeather(cityName, cityWeatherStationID)

                # Enrich with sentiment
                sentiment.enrichWithSentiment(cityName)

                # Clean data
                clean.clean(cityName)


def cityDataExists():
    return os.path.isfile(cityName + '.json')


enrichAllPlaces()
