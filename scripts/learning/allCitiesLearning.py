from scripts.machineLearning import train
from scripts.sentiment import sentiment
from scripts.twitter import twitterAPI
from scripts.utils import utils
import json

from scripts.weather import augmentWeather
import json

with open(utils.getFullPathFromDataFileName('places.json')) as data_file:
    places = json.load(data_file)

# Get twitter data for city
city = places[6]
cityName = city["name"]
cityProperName = city["properName"]
cityBoundingBox = city["boundingBox"]
cityWeatherStationID = city["weatherStationID"]

newYork = json.loads(open(utils.getFullPathFromDataFileName("manhattan_weather_sentiment.json")).read())
chicago = json.loads(open(utils.getFullPathFromDataFileName("chicago_weather_sentiment.json")).read())
detroit = json.loads(open(utils.getFullPathFromDataFileName("detroit_weather_sentiment.json")).read())

def combine_dicts(*dicts):
    return reduce(lambda dict1, dict2: dict(zip(dict1.keys() + dict2.keys(), dict1.values() + dict2.values())), dicts)

final = []
final.extend(newYork)
final.extend(chicago)
final.extend(detroit)

allJsonPath = utils.getFullPathFromDataFileName("all.json")
obj = open(allJsonPath, 'wb')
obj.write(json.dumps(final))
obj.close
# twitterAPI.saveTweets(5, cityName, cityBoundingBox, cityProperName)
# twitterDataRawPath = utils.getFullPathFromDataFileName(cityName + 'Raw.json')
# twitterDataPath = utils.getFullPathFromDataFileName("all" + '.json')
# twitterDataPath = utils.exportMongoOutputToJson(twitterDataRawPath, twitterDataPath)



# # Enrich with weather data
# twitterWeatherDataPath = augmentWeather.enrichWithWeather(location_name=cityName, stationID=cityWeatherStationID)
#
# # Enrich with sentiment
# twitterWeatherSentimentDataPath = utils.getFullPathFromDataFileName(cityName + '_weather_sentiment.json')
# sentiment.enrichWithSentiment(twitterWeatherDataPath, twitterWeatherSentimentDataPath)
#
# # Do machine learning
results = train.runClassifier(allJsonPath,,