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
        sum = 0
        placeCounts = []
        for place in places:
            cityName = place["name"]
            cityProperName = place["properName"]

            if cityDataExists(cityName):
                count = countGroupData(cityName)
                placeCounts.append((cityProperName, count))
                sum = sum + count
            else:
                print 'No data file found for: ', cityProperName
        placeCountsSorted = sorted(((v, k) for k, v in placeCounts), reverse=True)
        for key, value in placeCountsSorted:
            print value + ': ' + str(key)
        print sum




def countData(cityName):
    inputPath = utils.getFullPathFromDataFileName(cityName + '.json')
    with open(inputPath) as data_file:
        dataEntries = json.load(data_file)
        return len(dataEntries)


def countGroupData(cityName):
    inputPath = utils.getFullPathFromDataFileName(cityName + '_weather_sentiment_clean_grouped.json')
    with open(inputPath) as data_file:
        dataEntries = json.load(data_file)
        for data in dataEntries:
            if data['sentiment_average'] < -1 or data['sentiment_average'] > 1:
                print 'average is bad'
                print data
            if data['sentiment_percent_positive'] < 0 or data['sentiment_percent_positive'] > 1:
                print 'percent is bad:'
                print data

        return len(dataEntries)


def countRedditData():
    # inputPath = utils.getFullPathFromDataFileName('reddit/allRedditComments.json')
    # inputPath = utils.getFullPathFromDataFileName('reddit/allRedditComments_weather.json')
    # inputPath = utils.getFullPathFromDataFileName('reddit/allRedditComments_weather_sentiment.json')
    # inputPath = utils.getFullPathFromDataFileName('reddit/allRedditComments_weather_sentiment_clean.json')
    inputPath = utils.getFullPathFromDataFileName('reddit/allRedditComments_weather_sentiment_clean_grouped.json')
    dataEntries = json.load(open(inputPath))
    counts = {}
    # cityKey = 'city'
    cityKey = 'location'
    for dataEntry in dataEntries:
        city = dataEntry[cityKey]
        if city not in counts:
            counts[city] = {}
            counts[city]['count'] = 1
            counts[city]['weatherCount'] = 1
        else:
            counts[city]['count'] = counts[city]['count'] + 1
            if 'temperature' in dataEntry:
                counts[city]['weatherCount'] = counts[city]['weatherCount'] + 1
    print counts
    print len(dataEntries)
    return len(dataEntries)


def cityDataExists(cityName):
    cityFileName = cityName + '.json'
    cityFilePath = utils.getFullPathFromDataFileName(cityFileName)
    return os.path.isfile(cityFilePath)


countRedditData()