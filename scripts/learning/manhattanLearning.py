from sklearn.ensemble import RandomForestClassifier

from scripts.machineLearning import train
from scripts.sentiment import sentiment
from scripts.twitter import twitterAPI
from scripts.utils import utils
import json

from scripts.weather import augmentWeather

with open(utils.getFullPathFromDataFileName('places.json')) as data_file:
    places = json.load(data_file)

# Get twitter data for city
city = places[0]
cityName = city["name"]
cityProperName = city["properName"]
cityBoundingBox = city["boundingBox"]
cityWeatherStationID = city["weatherStationID"]
# twitterAPI.saveTweets(5, cityName, cityBoundingBox, cityProperName)
# twitterDataPath = utils.exportMongoCollectionToJson('twitterData', cityName, cityName)
#
# # Enrich with weather data
# twitterWeatherDataPath = augmentWeather.enrichWithWeather(location_name=cityName)
#
# # Enrich with sentiment
# twitterWeatherDataPath = utils.getFullPathFromDataFileName(cityName + '_weather.json')
twitterWeatherSentimentFileName = cityName + '_weather_sentiment.json'
# print twitterWeatherDataPath
# print twitterWeatherSentimentDataPath
# sentiment.enrichWithSentiment(twitterWeatherDataPath, twitterWeatherSentimentDataPath)
#
# # Do machine learning

classifier = RandomForestClassifier(
    n_estimators=10
)
print ''
print 'About to do machine learning on file: ', twitterWeatherSentimentFileName
results = train.runClassifier(classifier, "randomForest", [twitterWeatherSentimentFileName])