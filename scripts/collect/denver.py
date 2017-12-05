from scripts.collect.twitter.twitterAPI import saveTweets

numTweetsToCapture = 10000000
mongoCollectionName = 'denver'
locationCoordinates = [
      -105.109815,
      39.614151,
      -104.734372,
      39.812975
    ]
locationName = 'denver'
saveTweets(numTweetsToCapture, mongoCollectionName, locationCoordinates, locationName)