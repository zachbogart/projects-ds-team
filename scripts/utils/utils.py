import os

from bson import json_util
from pymongo import MongoClient
import json

from scripts.utils.definitions import ROOT_DIRECTORY, DATA_DIRECTORY, RESOURCE_DIRECTORY, RESULT_DIRECTORY


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
    obj.close()
    return fullPath

def exportMongoOutputToJson(inputFilePath, outputFilePath):
    with open(inputFilePath) as data_file:
        resultsJson = json_util.dumps(data_file)
        # resultsJson = json_util.dumps(data_file)

    # resultsJson = resultsJson.replace('\\"', '"')
    # resultsJson = resultsJson.replace('\\', '"')
    jsonObject = json.loads(resultsJson)
    # resultsJson = json.dumps(d)
    # output = []

    obj = open(outputFilePath, 'wb')
    obj.write('[')
    count = 0
    for result in jsonObject:
        if count is not 0:
            obj.write(',')
        else:
            count = 1
        obj.write(str(result.encode('utf-8')))
    # output = json.dumps(output)
    # obj.write(str(resultsJson.encode('utf-8')))
    obj.write(']')
    obj.close()
    return outputFilePath

def makeFullPath(pathFromScripts):
    return os.path.join(ROOT_DIRECTORY, pathFromScripts)

def getFullPathFromDataFileName(dataFileName):
    return DATA_DIRECTORY + '/' + dataFileName

def getFullPathFromResourceFileName(resourceFileName):
    return RESOURCE_DIRECTORY + '/' + resourceFileName

def getFullPathFromResultFileName(resourceFileName):
    return RESULT_DIRECTORY + '/' + resourceFileName
