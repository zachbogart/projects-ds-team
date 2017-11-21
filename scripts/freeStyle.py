import json

from scripts.machineLearning import train
from scripts.sentiment import sentiment
from scripts.twitter import twitterAPI
from scripts.utils import utils

# nycBoundingBox = [
#             -74.026675,
#             40.683935,
#             -73.910408,
#             40.877483
#         ]
# twitterAPI.saveTweets(5, nycBoundingBox, 'manhattan', "Manhattan")
# mongoToJson.exportMongoCollectionToJson('twitterData', 'manhattan', 'manhattan')

# twitterAPI.getTweetsAndSaveToJson()

# twitterAPI.getPlaceID("Detroit")
# twitterAPI.getNYCTweets()


# fetchWeather.parse_data(2017, 2017, 725030)
# fetchWeather.parse_data(2017, 2017, "725030-14732")


# train.doMachineLearning("../data/trainingData.json")

# def learningFunction():
#     return train.doMachineLearning("../data/trainingData.json")
#
# minTime = timeit.timeit(learningFunction, number=10)
#
# print ''
# print "minTime"
# print minTime


# IDEAL CODE
# ________________________

# Import places
from scripts.weather import augmentWeather

with open(utils.getFullPathFromDataFileName('places.json')) as data_file:
    places = json.load(data_file)

# Get twitter data for city
city = places[0]
cityName = city["name"]
cityProperName = city["properName"]
cityBoundingBox = city["boundingBox"]
cityWeatherStationID = city["weatherStationID"]
twitterAPI.saveTweets(50000, cityName, cityBoundingBox, cityProperName)
# # twitterDataPath = utils.exportMongoCollectionToJson('twitterData', cityName, cityName)
# #
# # # Enrich with weather data
# # twitterWeatherDataPath = augmentWeather.enrichWithWeather(location_name=cityName)
# twitterWeatherDataPath = augmentWeather.enrichWithWeather(location_name=cityName, stationID=cityWeatherStationID)
# #
# # # Enrich with sentiment
# twitterWeatherSentimentDataPath = utils.getFullPathFromDataFileName(cityName + '_weather_sentiment.json')
# sentiment.enrichWithSentiment(twitterWeatherDataPath, twitterWeatherSentimentDataPath)
# #
# # # Do machine learning
# results = train.runClassifier(twitterWeatherSentimentDataPath,,



# with open(utils.makeDataFilePath('places.json')) as data_file:
#     places = json.load(data_file)
#
# def acquireData(placesIndex):
#     city = places[placesIndex]
#     cityName = city["name"]
#     cityProperName = city["properName"]
#     cityBoundingBox = city["boundingBox"]
#     twitterAPI.saveTweets(1000000, cityName, cityBoundingBox, cityProperName)
#     pathToJson = utils.exportMongoCollectionToJson('twitterData', cityName, cityName)
