from scripts.twitter import mongoToJson, twitterAPI
from weather import fetchWeather
from scripts.machineLearning import train

# nycBoundingBox = [
#             -74.026675,
#             40.683935,
#             -73.910408,
#             40.877483
#         ]
# twitterAPI.saveTweets(5, nycBoundingBox, 'manhattan')
# mongoToJson.exportMongoCollectionToJson('twitterData', 'manhattan', 'manhattan')

# twitterAPI.getTweetsAndSaveToJson()

# twitterAPI.getPlaceID()
# twitterAPI.getNYCTweets()


# fetchWeather.parse_data(2017, 2017, 725030)
# fetchWeather.parse_data(2017, 2017, "725030-14732")


train.doMachineLearning("../data/trainingData.json")