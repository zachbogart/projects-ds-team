import os

from bson import json_util
from pymongo import MongoClient

from scripts.utils.definitions import ROOT_DIRECTORY, DATA_DIRECTORY, RESOURCE_DIRECTORY


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

    fullPath = getFullPathFromDataFileName(resultFileName + '.json')
    obj = open(fullPath, 'wb')
    obj.write(resultsJson)
    obj.close
    return fullPath

def makeFullPath(pathFromScripts):
    return os.path.join(ROOT_DIRECTORY, pathFromScripts)

def getFullPathFromDataFileName(dataFileName):
    return DATA_DIRECTORY + '/' + dataFileName

def getFullPathFromResourceFileName(resourceFileName):
    return RESOURCE_DIRECTORY + '/' + resourceFileName
