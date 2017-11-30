

import urllib
import requests
import json
import time as tm

def getWeatherForCoordinates(gps):
    base_url = 'https://api.darksky.net/forecast/daa6fec58a10641303d2fe57266d1f27/'

    hourlyWeather = dict()

    startDay = 1508889600
    endDay = 1511991800

    for t in range(startDay,endDay,86400):
        url = base_url + gps + ',' + str(t)
        day = tm.strftime('%Y-%m-%d', tm.localtime(t))
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        hourly = data['hourly']
        hourlyWeather[day] = (hourly)

    return hourlyWeather

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

    
