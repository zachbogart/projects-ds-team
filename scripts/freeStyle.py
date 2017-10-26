from scripts.twitter import mongoToJson, twitterAPI
from weather import fetchWeather
from scripts.machineLearning import train

# nycBoundingBox = [
#             -74.026675,
#             40.683935,
#             -73.910408,
#             40.877483
#         ]
# twitterAPI.saveTweets(5, nycBoundingBox, 'manhattan', "Manhattan")
# mongoToJson.exportMongoCollectionToJson('twitterData', 'manhattan', 'manhattan')

# places = [
#     {
#         "name": "manhattan",
#         "boundingBox": [
#             -74.026675,
#             40.683935,
#             -73.910408,
#             40.877483
#         ],
#         "weatherStationID": "725030-14732"
#     }
# ]

# twitterAPI.getTweetsAndSaveToJson()

# twitterAPI.getPlaceID("San Fransisco")
# twitterAPI.getNYCTweets()


# fetchWeather.parse_data(2017, 2017, 725030)
# fetchWeather.parse_data(2017, 2017, "725030-14732")


train.doMachineLearning("../data/trainingData.json")
