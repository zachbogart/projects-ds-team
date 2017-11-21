from scripts.machineLearning import train
from scripts.sentiment import sentiment
from scripts.twitter import twitterAPI
from scripts.utils import utils
import json

from scripts.weather import augmentWeather

with open(utils.getFullPathFromDataFileName('places.json')) as data_file:
    places = json.load(data_file)

# Get twitter data for city
city = places[6]
cityName = city["name"]
cityProperName = city["properName"]
cityBoundingBox = city["boundingBox"]
cityWeatherStationID = city["weatherStationID"]
# twitterAPI.saveTweets(5, cityName, cityBoundingBox, cityProperName)
# twitterDataRawPath = utils.getFullPathFromDataFileName(cityName + 'Raw.json')
# twitterDataPath = utils.getFullPathFromDataFileName(cityName + '.json')
# twitterDataPath = utils.exportMongoOutputToJson(twitterDataRawPath, twitterDataPath)

# Enrich with weather data
twitterWeatherDataPath = augmentWeather.enrichWithWeather(location_name=cityName, stationID=cityWeatherStationID)

# Enrich with sentiment
twitterWeatherSentimentDataPath = utils.getFullPathFromDataFileName(cityName + '_weather_sentiment.json')
sentiment.enrichWithSentiment(twitterWeatherDataPath, twitterWeatherSentimentDataPath)

# Do machine learning
results = train.runClassifier(twitterWeatherSentimentDataPath,,