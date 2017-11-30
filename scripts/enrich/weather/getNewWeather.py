

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