# from scripts.twitter import mongoToJson, twitterAPI
from weather import fetchWeather
from scripts.machineLearning import train
import timeit


# nycBoundingBox = [
#             -74.026675,
#             40.683935,
#             -73.910408,
#             40.877483
#         ]
# twitterAPI.saveTweets(5, nycBoundingBox, 'manhattan', "Manhattan")
# mongoToJson.exportMongoCollectionToJson('twitterData', 'manhattan', 'manhattan')

places = [
    {
        "name": "manhattan",
        "properName": "Manhattan",
        "boundingBox": [
            -74.026675,
            40.683935,
            -73.910408,
            40.877483
        ],
        "weatherStationID": "725030-14732"
    }
]

# twitterAPI.getTweetsAndSaveToJson()

# twitterAPI.getPlaceID("San Fransisco")
# twitterAPI.getNYCTweets()


# fetchWeather.parse_data(2017, 2017, 725030)
# fetchWeather.parse_data(2017, 2017, "725030-14732")


train.doMachineLearning("../data/trainingData.json")

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
#
# Get twitter data for city
# city = places[0]
# cityName = city["name"]
# cityProperName = city["properName"]
# cityBoundingBox = city["boundingBox"]
# twitterAPI.saveTweets(5000000, cityName, cityBoundingBox, cityProperName)
# pathToJson = mongoToJson.exportMongoCollectionToJson('twitterData', cityName, cityName)
#
# Enrich with weather data
# weather.enrichWithWeather(pathToJson, cityName)
#
# Enrich with sentiment
# sentiment.enrichWithSentiment(pathToJson)
#
# Do machine learning
# results = train.doMachineLearning(pathToJson)
#
#
