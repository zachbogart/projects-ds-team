

import urllib
import requests
import json
import time as tm

from scripts.utils import utils


def getPresavedWeatherData(gps):
    weatherDataPath = utils.getFullPathFromDataFileName('weather/weatherData_' + gps + '.json')
    data_file = open(weatherDataPath)
    json_data = json.load(data_file)
    return json_data


def savePresavedWeatherData(gps, json_data):
    weatherDataPath = utils.getFullPathFromDataFileName('weather/weatherData_' + gps + '.json')
    with open(weatherDataPath, 'w') as outfile:
        json.dump(json_data, outfile)


def getWeatherForCoordinates(gps):
    base_url = 'https://api.darksky.net/forecast/daa6fec58a10641303d2fe57266d1f27/'

    may012015 = 1430452800
    oct252017 = 1508889600
    nov302017 = 1511991800
    oneDayInSeconds = 86400

    presavedWeather = getPresavedWeatherData(gps)
    weatherChanged = False

    for t in range(may012015, nov302017, oneDayInSeconds):
        url = base_url + gps + ',' + str(t)
        day = tm.strftime('%Y-%m-%d', tm.localtime(t))
        if day in presavedWeather:
            data = presavedWeather[day]['hourly']
        else:
            response = urllib.urlopen(url)
            if response.code == 403:
                raise Exception("Weather API call received 403 Error")
            data = json.loads(response.read())
            hourly = data['hourly']
            presavedWeather[day] = hourly
            weatherChanged = True

    if weatherChanged:
        savePresavedWeatherData(gps, presavedWeather)
    return presavedWeather

def handleNansInDict(json_file):
    data_file = open(json_file)
    json_data = json.load(data_file)
    
#     nans = df[df.isnull().any(axis=1)]
#     print "Here are the columns containing Nans :"
#     print pd.isnull(nans).sum() > 0
    
    for i in range(len(json_data)):
        d = json_data[i]

    # precipType: set value to 'NoPrecip'
        if 'precipType' not in d.keys():
            d['precipType'] = 'NoPrecip'
        
    # remove ozone, windGusts and uv index from the dataframe
        try:
            del d['ozone']
        except KeyError:
            pass
        try:
            del d['uvIndex']
        except KeyError:
            pass
        try:
            del d['windGust']
        except KeyError:
            pass
        
    #handle cloudCover
        iconDict = {'fog': .5,'clear-night': 0,'clear-day': 0, 'partly-cloudy-day': .5, 'cloudy': .8, u'partly-cloudy-night': .5, 'wind': .5, 'rain': .7}
    
        if 'cloudCover' not in d.keys():
            d['cloudCover'] = iconDict[d['icon']]
    
    json_data[i] = d
    
    outputPath = json_file[:-5] + 'er.json'
    with open(outputPath, 'w') as outfile:
        json.dump(json_data, outfile)

    
