# coding: utf-8

# In[14]:

############### READ ME ##############################
# usage: 
# input (default values show): augmentWeather(start_year=2017,end_year=2017,stationID='725030-14732',location_name='manhattan', root_path='../../')
# output: json file saved in data directory "locationName_weather.json"
# output: returns DataFrame of the same data

# stationID='998479-99999',location_name='sanFrancisco'
# stationID='725030-14732',location_name='manhattan'
#####################################################


# In[15]:
import json

from scripts.enrich.weather import getNewWeather
from scripts.utils import utils


def getWeather(created_at, weather):
    from datetime import datetime
    d = str(created_at)
    d = int(d[:10])
    tweet_year = datetime.fromtimestamp(d).strftime('%Y')
    tweet_month = datetime.fromtimestamp(d).strftime('%m')
    tweet_day = datetime.fromtimestamp(d).strftime('%d')
    tweet_hour = int(datetime.fromtimestamp(d).strftime('%I'))

    weatherKey = tweet_year + '-' + tweet_month + '-' + tweet_day
    weatherDataDaily = weather[weatherKey]['data']
    weatherDataHourly = weatherDataDaily[tweet_hour]
    return weatherDataHourly


# In[16]:

def enrichWithWeather(location_name, coordinates):
    weather = getNewWeather.getWeatherForCoordinates(coordinates)
    print 'weather length = ' + str(len(weather)) + ' days of data'

    dataFilePath = utils.getFullPathFromDataFileName(location_name + '.json')
    with open(dataFilePath) as data_file:
        jsonData = json.load(data_file)
        print 'Adding weather to data of length = ' + str(len(jsonData))

    count = 0
    for dataObject in jsonData:
        if count % 100000 == 0:
            print "Adding weather data: ", count
        count = count + 1

        datetime = dataObject['created_at']['$date']
        tweetWeather = getWeather(datetime, weather)

        dataObject.update(tweetWeather)

    outputPath = utils.getFullPathFromDataFileName(location_name + '_weather.json')
    print 'Saving file: ', outputPath
    with open(outputPath, 'w') as outfile:
        json.dump(jsonData, outfile)

    print 'Saved file: ', outputPath

    return outputPath
