
# coding: utf-8

# In[ ]:


from twitter import mongoToJson, twitterAPI

nycBoundingBox = [
            -74.026675,
            40.683935,
            -73.910408,
            40.877483
        ]
twitterAPI.saveTweets(2000, 'manhattan', nycBoundingBox)
mongoToJson.exportMongoCollectionToJson('twitterData', 'manhattan', 'manhattan')

