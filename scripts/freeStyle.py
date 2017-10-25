from scripts.twitter import mongoToJson, twitterAPI

nycBoundingBox = [
            -74.026675,
            40.683935,
            -73.910408,
            40.877483
        ]
twitterAPI.saveTweets(5, nycBoundingBox, 'manhattan')
mongoToJson.exportMongoCollectionToJson('twitterData', 'manhattan', 'manhattan')

# twitterAPI.getTweetsAndSaveToJson()

# twitterAPI.getPlaceID()
# twitterAPI.getNYCTweets()