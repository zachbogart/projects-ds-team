from scripts.twitter import mongoToJson, twitterAPI

twitterAPI.saveTweets(20, ['deadpool', 'spider-man', 'iron man'], 'marvelComics')
mongoToJson.exportMongoCollectionToJson('twitterData', 'marvelComics', 'marvelComics')

# twitterAPI.saveTweets(3, ['#NationalFoodDay'], 'nationalFoodDay')
# mongoToJson.exportMongoCollectionToJson('twitterData', 'nationalFoodDay', 'nationalFoodDay')
