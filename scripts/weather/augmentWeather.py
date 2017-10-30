
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
from scripts.utils import utils


def getWeather(created_at, weather):
    from datetime import datetime
    d=str(created_at)
    d = int(d[:10])
    tweet_year = int(datetime.fromtimestamp(d).strftime('%Y'))
    tweet_month = int(datetime.fromtimestamp(d).strftime('%m')) # '%m-%d %I:%M:%S %p'
    tweet_day = int(datetime.fromtimestamp(d).strftime('%d'))
    tweet_hour = int(datetime.fromtimestamp(d).strftime('%I'))
    
    weather_data = weather[(weather.month == tweet_month) & (weather.day == tweet_day) & (weather.hour == tweet_hour)]
    return weather_data 


# In[16]:

def enrichWithWeather(start_year=2017, end_year=2017, stationID='725030-14732', location_name='manhattan'):
    import json
    import pandas as pd
    from fetchWeather import parse_data
#     reload(fetchWeather)
    
    weather = parse_data(start_year,end_year,stationID)
    print 'weather length = ' + str(len(weather))

    dataFilePath = utils.getFullPathFromDataFileName(location_name + '.json')
    with open(dataFilePath) as data_file:
            jsonData = json.load(data_file)
            print 'jsonData Length = ' + str(len(jsonData))
            
    for i in jsonData:
        datetime = i['created_at']['$date']
        tweetWeather = getWeather(datetime,weather)
        
        for col in weather.columns:
            i[col] = int(tweetWeather[col])

    outputPath = utils.getFullPathFromDataFileName(location_name + '_weather.json')
    with open(outputPath, 'w') as outfile:
        json.dump(jsonData, outfile)

    return outputPath

