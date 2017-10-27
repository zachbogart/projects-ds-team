# from scripts.twitter import mongoToJson, twitterAPI
# from scripts.weather import fetchWeather
import twitter.twitterAPI as twitterAPI

from machineLearning import train
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
        "weatherStationID": "725033-99999"
    },
    {
        "name": "sanFrancisco",
        "properName": "San Francisco",
        "boundingBox": [
            -122.514926,
            37.708075,
            -122.357031,
            37.833238
        ],
        "weatherStationID": "994016-99999"
    },
    {
        "name": "washingtonDC",
        "properName": "Washington DC",
        "boundingBox": [
            -77.119401,
            38.801826,
            -76.909396,
            38.9953797
        ],
        "weatherStationID": "997314-99999"
    },
    {
        "name": "houston",
        "properName": "Houston",
        "boundingBox": [
            -95.823268,
            29.522325,
            -95.069705,
            30.1546646
        ],
        "weatherStationID": "720594-00188"
    },
    {
        "name": "denver",
        "properName": "Denver",
        "boundingBox": [
            -105.109815,
            39.614151,
            -104.734372,
            39.812975
        ],
        "weatherStationID": "999999-23012"
    },
    {
        "name": "seattle",
        "properName": "Seattle",
        "boundingBox": [
            -122.436232,
            47.4953154,
            -122.2249728,
            47.734319
        ],
        "weatherStationID": "994014-99999"
    },
    {
        "name": "chicago",
        "properName": "Chicago",
        "boundingBox": [
            -87.940033,
            41.644102,
            -87.523993,
            42.0230669
        ],
        "weatherStationID": "725346-94866"
    },
    {
        "name": "boston",
        "properName": "Boston",
        "boundingBox": [
            -71.191421,
            42.227797,
            -70.986004,
            42.399542
        ],
        "weatherStationID": "994971-99999"
    },
    {
        "name": "newOrleans",
        "properName": "New Orleans",
        "boundingBox": [
            -90.137908,
            29.889574,
            -89.884108,
            30.075628

        ],
        "weatherStationID": "722310-12916"
    },
    {
        "name": "lasVegas",
        "properName": "Las Vegas",
        "boundingBox": [
            -115.384091,
            36.129459,
            -115.062159,
            36.336371

        ],
        "weatherStationID": "724846-53123"
    },
    {
        "name": "phoenix",
        "properName": "Phoenix",
        "boundingBox": [
            -112.3239143,
            33.29026,
            -111.9254391,
            33.8154652

        ],
        "weatherStationID": "722780-23183"
    },
    {
        "name": "jacksonville",
        "properName": "Jacksonville",
        "boundingBox": [
            30.209491,
            -81.861674,
            30.519937,
            -81.482646

        ],
        "weatherStationID": "722065-93837"
    },
    {
        "name": "detroit",
        "properName": "Detroit",
        "boundingBox": [
            -83.288056,
            42.255085,
            -82.91052,
            42.450488

        ],
        "weatherStationID": "999999-14822"
    }
]

# twitterAPI.getTweetsAndSaveToJson()

twitterAPI.getPlaceID("Detroit")
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
