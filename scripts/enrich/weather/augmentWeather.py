# coding: utf-8

############### READ ME ##############################
# usage: 
# input (default values show): augmentWeather(start_year=2017,end_year=2017,stationID='725030-14732',location_name='manhattan', root_path='../../')
# output: json file saved in data directory "locationName_weather.json"
# output: returns DataFrame of the same data

# stationID='998479-99999',location_name='sanFrancisco'
# stationID='725030-14732',location_name='manhattan'
#####################################################


import json

import math

from scripts.enrich.weather import getNewWeather
from scripts.utils import utils


def getWeatherAtDatetime(created_at, weather):
    from datetime import datetime
    d = str(int(created_at))
    d = int(d[:10])
    tweet_year = datetime.fromtimestamp(d).strftime('%Y')
    tweet_month = datetime.fromtimestamp(d).strftime('%m')
    tweet_day = datetime.fromtimestamp(d).strftime('%d')
    tweet_hour = int(datetime.fromtimestamp(d).strftime('%I'))

    weatherKey = tweet_year + '-' + tweet_month + '-' + tweet_day
    if weatherKey not in weather:
        print ''
        # print weather
        # print ''
        print weatherKey
        if int(tweet_year) <= 2015 and int(tweet_month) <= 4 or int(tweet_year) < 2015:
            return []
        else:
            raise Exception("No Weather for this: " + weatherKey)
    else:
        weatherDataDaily = weather[weatherKey]['data']
        weatherDataHourly = weatherDataDaily[tweet_hour]
        return weatherDataHourly


def enrichWithWeather(location_name, coordinates):
    actualCityNameMap = {
        'chicago': 'chicago',
        'asburypark': 'asburyPark',
        'denver': 'denver',
        'detroit': 'detroit',
        'houston': 'houston',
        'nyc': 'manhattan',
        'phoenix': 'phoenix',
        'sanfrancisco': 'sanFrancisco',
        'san francisco': 'sanFrancisco',
        'seattle': 'seattle',
        'manhattan': 'manhattan'
    }
    locationWeatherDictionary = {}
    print 'Getting weather data'
    if type(coordinates) == unicode:
        # weather = None
        weather = getNewWeather.getWeatherForCoordinates(coordinates)
        locationWeatherDictionary[location_name] = weather
    else:
        for place, coordinate in coordinates.iteritems():
            weather = getNewWeather.getWeatherForCoordinates(coordinate)
            # weather = None
            locationWeatherDictionary[place] = weather

    dataFilePath = utils.getFullPathFromDataFileName(location_name + '.json')
    with open(dataFilePath) as data_file:
        jsonData = json.load(data_file)
        print 'Adding weather to data of length = ' + str(len(jsonData))

        count = 0
        for dataObject in jsonData:
            if count % 100000 == 0:
                print "Adding weather data: ", count
            count = count + 1
            if 'created' in dataObject:
                datetime = dataObject['created']
                city_ = str(dataObject['city'].lower().strip())
            else:
                datetime = dataObject['created_at']['$date']
                if 'location' not in dataObject:
                    dataObject['location'] = location_name
                city_ = str(dataObject['location'].lower().strip())
            # try:
            place = actualCityNameMap[city_]
            weather = locationWeatherDictionary[place]
            tweetWeather = getWeatherAtDatetime(datetime, locationWeatherDictionary[place])

            dataObject.update(tweetWeather)
            # except:
            #     print city_

        outputPath = utils.getFullPathFromDataFileName(location_name + '_weather.json')
        print 'Saving file: ', outputPath
        with open(outputPath, 'w') as outfile:
            json.dump(jsonData, outfile)

    print 'Saved file: ', outputPath

    return outputPath
