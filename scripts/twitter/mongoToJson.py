
# coding: utf-8

# In[ ]:


from pymongo import MongoClient
from bson import json_util
import json


def exportMongoCollectionToJson(mongoDatabaseName, mongoCollectionName, resultFileName):
    print 'About to connect to Mongo'
    mongo = MongoClient('localhost', 27017)
    mongo_db = mongo[mongoDatabaseName]
    mongo_collection = mongo_db[mongoCollectionName]
#     print 'Connection made to:'
#     print 'db name: ' + mongo_db.name
#     print 'collection name: ' + mongo_collection.name

    results = mongo_collection.find({})
    resultsJson = json_util.dumps(results)

    pathToDataFolder = '/home/rij2105/twitterDataJson/'
    fullPath = pathToDataFolder + resultFileName + '.json'
    obj = open(fullPath, 'wb')
    obj.write(resultsJson)
    obj.close
#     print 'File saved at path: ' + fullPath

