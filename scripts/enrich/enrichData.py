import json

import os
import pandas as pd
import time

from scripts.enrich.clean import clean
from scripts.enrich.weather import augmentWeather
from scripts.enrich.sentiment import sentiment
from scripts.learn import machineLearning
from scripts.utils import utils


def enrichAllPlaces():
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

                # # Enrich with weather data
                # print 'Enriching with Weather Data'
                # augmentWeather.enrichWithWeather(cityName, coordinates)

                # # Enrich with sentiment
                # print 'Enriching with Sentiment'
                # sentiment.enrichWithSentiment(cityName)
                #
                # # Clean data
                # print 'Cleaning Data'
                # clean.clean(cityName)

                # Group Data
                print 'Grouping Data'
                groupDataByHour(cityName)

            else:
                print 'No data file found for: ', cityProperName


def enrichAllRedditPlaces():
    with open(utils.getFullPathFromDataFileName('places.json')) as data_file:
        places = json.load(data_file)
        placeCoordinateDictionary = {}
        for place in places:
            cityName = place["name"]
            cityProperName = place["properName"]
            coordinates = place["coordinates"]
            placeCoordinateDictionary[cityName] = str(coordinates)

        print ''
        print ''
        print 'About to enrich all reddit data'

        fileName = 'reddit/allRedditComments'

        # Enrich with weather data
        print 'Enriching with Weather Data'
        augmentWeather.enrichWithWeather(fileName, placeCoordinateDictionary)

        # Enrich with sentiment
        print 'Enriching with Sentiment'
        sentiment.enrichWithSentiment(fileName)

        # Clean data
        print 'Cleaning Data'
        clean.clean(fileName)

        # Group Data
        print 'Grouping Data'
        groupDataByHour(fileName)


def groupDataByHour(cityName):
    inputPath = utils.getFullPathFromDataFileName(cityName + '_weather_sentiment_clean.json')
    outputPath = utils.getFullPathFromDataFileName(cityName + '_weather_sentiment_clean_grouped.json')
    print 'Opening data from: ', inputPath
    with open(inputPath) as data_file:
        dataEntries = json.load(data_file)
        print 'Data of length: ', len(dataEntries)

        count = 0
        groupedData = {}
        for dataEntry in dataEntries:
            if count % 100000 == 0:
                print "Grouping data -- count: ", count
            count = count + 1

            sentiment = dataEntry['sentiment']
            sentimentScore = float(dataEntry['sentimentScore'])
            if 'location' in dataEntry:
                location = dataEntry['location']
            elif 'city' in dataEntry:
                location = dataEntry['city']
            timeHour = time.strftime('%Y-%m-%d %H', time.localtime(dataEntry['created']))
            groupKey = makeUniqueKey(timeHour, location)
            if groupKey in groupedData:
                if groupedData[groupKey]['temperature'] != dataEntry['temperature']:
                    print ''
                    print 'This data entry is wrong'
                    print dataEntry

                oldCount = groupedData[groupKey]['num_data']
                newCount = oldCount + 1.0

                oldSentimentAverageScore = groupedData[groupKey]['sentiment_percent_positive']
                newSentimentAverageScore = ((oldSentimentAverageScore * oldCount) + sentimentScore) / newCount
                groupedData[groupKey]['sentiment_percent_positive'] = newSentimentAverageScore

                oldSentimentAverage = groupedData[groupKey]['sentiment_average']
                newSentimentAverage = ((oldSentimentAverage * oldCount) + sentiment) / newCount
                groupedData[groupKey]['sentiment_average'] = newSentimentAverage

                groupedData[groupKey]['num_data'] = newCount

            else:
                weatherColumnNames = [
                    'cloudCover',
                    'temperature',
                    'dewPoint',
                    'visibility',
                    'apparentTemperature',
                    'pressure',
                    'precipIntensity',
                    'precipTypeNone',
                    'precipTypeRain',
                    'precipTypeSnow',
                    'humidity',
                    'windSpeed',
                    'precipProbability',
                    'precipType',
                    'icon',
                ]
                newDataEntry = {
                    'timeHour': timeHour,
                    'created': dataEntry['created'],
                    'time': dataEntry['time'],
                    'sentiment_average': sentiment,
                    'sentiment_percent_positive': sentimentScore,
                    'num_data': 1.0
                }
                if 'location' in dataEntry:
                    newDataEntry['location'] = location
                elif 'city' in dataEntry:
                    newDataEntry['location'] = location
                for weatherColumn in weatherColumnNames:
                    newDataEntry[weatherColumn] = dataEntry[weatherColumn]
                groupedData[groupKey] = newDataEntry

        print 'Saving file: ', outputPath
        print '# values: ', str(len(groupedData))
        with open(outputPath, 'w') as outfile:
            groupedDataValues = groupedData.values()
            json.dump(groupedDataValues, outfile)

        print 'Saved file: ', outputPath

def makeUniqueKey(timeHour, location):
    return timeHour + location

def cityDataExists(cityName):
    cityFileName = cityName + '.json'
    cityFilePath = utils.getFullPathFromDataFileName(cityFileName)
    return os.path.isfile(cityFilePath)


# redditCsvToJson()
# enrichAllPlaces()
enrichAllRedditPlaces()
