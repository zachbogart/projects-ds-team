import json
import pandas as pd
import numpy as np
from bson import json_util
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor, VotingClassifier, BaggingClassifier, \
    ExtraTreesClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
from scripts.utils import utils
from time import time
from random import random

np.random.seed(7)
pd.options.mode.chained_assignment = None  # Removes unnecessary warning

featureColumnNames = [
    'cloudCover',
    # 'summary',
    'temperature',
    'dewPoint',
    # 'followers',
    # 'location',
    'windBearing',
    # 'local_datetime',
    # 'friends_count',
    # 'windGust', # Some nan values
    'visibility',
    'apparentTemperature',
    'pressure',
    # 'icon',
    'precipIntensity',
    'precipTypeNone',
    'precipTypeRain',
    'precipTypeSnow',
    'humidity',
    # 'ozone', # Some nan values
    'windSpeed',
    # 'uvIndex', # Some nan values
    'precipProbability',
]


def tuneParameters(parameterGrid, classifierName, classifier, jsonFileNames, numDataPoints):
    """
    This function should be called to find the best combination of
    parameters to run. Results will be written as csv file in the form
    <classifierName>_parameterTuning.csv

    Be careful of including too many parameters, this function will
    run EVERY combination of parameters. To find a smaller range of values
    for a parameter try running tuneParametersIndividually first

    :param parameterGrid: ex-- {
        nEstimators: [2,4,6,8],
        maxDepth: [1,10,100,1000]
    }
    :param classifierName: May not contain spaces
    :param classifier:
    :param jsonFileNames: ex-- [
        'chicago_weather_sentiment.json',
        'manhattan_weather_sentiment.json',
        'detroit_weather_sentiment.json'
    ]
    :param numDataPoints: The number of data points we will sample to run this
    """
    if ' ' in classifierName:
        raise Exception('No spaces allowed in classifierName')

    jsonData = retrieveJsonData(jsonFileNames)
    data = pd.DataFrame.from_dict(jsonData, orient='columns')
    data['sentimentScore'] = data['sentiment'].apply(isLabelPositive)
    data['sentimentLabel'] = data['sentimentScore'].apply(toLabelName)

    labelColumnName = 'sentimentScore'

    usableColumnNames = []
    usableColumnNames.extend(featureColumnNames)
    usableColumnNames.append(labelColumnName)

    usableData = data[usableColumnNames].dropna()
    smallerData = randomSampleDatapoints(usableData, numDataPoints)
    trainData = smallerData[featureColumnNames]
    trainLabels = smallerData[labelColumnName]

    numCombinations = computeNumCombinations(parameterGrid)
    print "About to tune parameters with # combinations: ", numCombinations

    results = evaluateParameters(classifier, trainData, trainLabels, parameterGrid)
    saveResultsAsCSV(results, classifierName, "parameterTuning")


def tuneParametersIndividually(parameterGrid, classifierName, classifier, jsonFileNames, numDataPoints):
    """
    This function will run through each parameter and try every value independent of any
    other variable. The result will be saved in separate files named
    <classifierName>_<parameter>.csv

    :param parameterGrid: ex-- {
        nEstimators: [2,4,6,8],
        maxDepth: [1,10,100,1000]
    }
    :param classifierName: May not contain spaces
    :param classifier:
    :param jsonFileNames: ex-- [
        'chicago_weather_sentiment.json',
        'manhattan_weather_sentiment.json',
        'detroit_weather_sentiment.json'
    ]
    :param numDataPoints: The number of data points we will sample to run this
    :return:
    """
    if ' ' in classifierName:
        raise Exception('No spaces allowed in classifierName')

    jsonData = retrieveJsonData(jsonFileNames)
    data = pd.DataFrame.from_dict(jsonData, orient='columns')
    data['sentimentScore'] = data['sentiment'].apply(isLabelPositive)
    data['sentimentLabel'] = data['sentimentScore'].apply(toLabelName)

    labelColumnName = 'sentimentScore'

    usableColumnNames = []
    usableColumnNames.extend(featureColumnNames)
    usableColumnNames.append(labelColumnName)

    usableData = data[usableColumnNames].dropna()
    smallerData = randomSampleDatapoints(usableData, numDataPoints)
    trainData = smallerData[featureColumnNames]
    trainLabels = smallerData[labelColumnName]

    for parameter, parameterOptions in dict.items(parameterGrid):
        print ''
        print "Running parameter: ", parameter
        results = evaluateParameter(classifier, trainData, trainLabels, parameter, parameterOptions)
        saveResultsAsCSV(results, classifierName, parameter)


def tuneNValue(nValues, classifier, classifierName, jsonFileNames):
    """
    This function will run the classifier for every n value and record the
    accuracy and time for each. The result will be saved in a file called
    <classifierName>_number_data_points.csv

    :param nValues: Values of n to run
    :param classifier:
    :param classifierName: May not contain spaces
    :return:
    """
    if ' ' in classifierName:
        raise Exception('No spaces allowed in classifierName')

    jsonData = retrieveJsonData(jsonFileNames)

    data = pd.DataFrame.from_dict(jsonData, orient='columns')
    data['sentimentScore'] = data['sentiment'].apply(isLabelPositive)
    data['sentimentLabel'] = data['sentimentScore'].apply(toLabelName)

    labelColumnName = 'sentimentScore'

    columnNames = []
    columnNames.extend(featureColumnNames)
    columnNames.append(labelColumnName)

    finalData = data[columnNames]
    datapointCount = len(finalData)
    print "We have " + str(datapointCount) + " total data points and will not run for n values greater than " + str(
        datapointCount)

    nValues = [x for x in nValues if x <= datapointCount]
    results = []
    for nValue in nValues:
        sampledData = randomSampleDatapoints(finalData, nValue)
        trainPercentage = .75
        trainData, testData, trainLabels, testLabels = train_test_split(sampledData[featureColumnNames],
                                                                        sampledData[labelColumnName],
                                                                        train_size=trainPercentage)
        print ''
        print 'Training n value', nValue

        startTime = time()
        classifier.fit(trainData, trainLabels)
        totalTime = time() - startTime
        predictions = classifier.predict(testData)
        testAccuracy = metrics.accuracy_score(testLabels, predictions)
        trainPredictions = classifier.predict(trainData)
        trainAccuracy = metrics.accuracy_score(trainLabels, trainPredictions)
        results.append({
            'time': totalTime,
            'testAccuracy': testAccuracy,
            'trainAccuracy': trainAccuracy
        })

    resultsDataFrame = pd.DataFrame(results)
    resultsDataFrame.index = nValues
    saveResultsAsCSV(resultsDataFrame, classifierName, 'number_data_points')


def runClassifier(classifier, classifierName, jsonFileNames, numDataPoints=None):
    """
    This function will run the provided classifier for a specific set of parameters
    Results will be saved to a file called <classifierName>_finalResults.csv

    :param classifierName: May not contain spaces
    :param classifier: Classifier should already be configured with parameters
    :param jsonFileNames:
    :param numDataPoints: Default is None. If not none, will sample the data and use only
                            given number of data points.
    :return:
    """
    if ' ' in classifierName:
        raise Exception('No spaces allowed in classifierName')

    jsonData = retrieveJsonData(jsonFileNames)

    data = pd.DataFrame.from_dict(jsonData, orient='columns')
    data['sentimentScore'] = data['sentiment'].apply(isLabelPositive)
    data['sentimentLabel'] = data['sentimentScore'].apply(toLabelName)

    labelColumnName = 'sentimentScore'

    usableColumnNames = []
    usableColumnNames.extend(featureColumnNames)
    usableColumnNames.append(labelColumnName)

    usableData = data[usableColumnNames].dropna()
    usableData = usableData[usableData['sentimentScore'] != 0]
    if numDataPoints != None:
        usableData = randomSampleDatapoints(usableData, numDataPoints)

    trainPercentage = .75
    trainData, testData, trainLabels, testLabels = train_test_split(usableData[featureColumnNames],
                                                                    usableData[labelColumnName],
                                                                    train_size=trainPercentage)
    print ''
    print('Number of observations in the training data:', len(trainData))
    print('Number of observations in the test data:', len(testData))

    print "Fitting ", classifierName
    classifier.fit(trainData, trainLabels)

    saveResultsFromTrainedClassifier(classifier, classifierName, trainData, trainLabels, testData, testLabels)


def computeNumCombinations(parameterGrid):
    numCombinations = 1
    for item in parameterGrid:
        numCombinations = numCombinations * len(parameterGrid[item])
    return numCombinations


def isLabelPositive(label):
    if label > 0:
        return 1
    elif label < 0:
        return -1
    else:
        raise Exception("This should not be 0. Neutral data should be removed")


def toLabelName(label):
    if label == 2:
        return 'negative'
    elif label == 0:
        return 'neutral'
    else:
        return 'positive'


def retrieveJsonData(jsonFileNames):
    results = []
    for jsonFileName in jsonFileNames:
        jsonPath = utils.getFullPathFromDataFileName(jsonFileName)
        with open(jsonPath) as dataFile:
            jsonData = json.load(dataFile)
        results.extend(jsonData)
    return results


def randomSampleDatapoints(data, sampleSize):
    if len(data) >= sampleSize:
        return data.sample(sampleSize)
    else:
        raise Exception('Not enough data to take a random sample of size: ', sampleSize)


def saveResultsAsCSV(parameterResults, classifierName, additionalName):
    resultsPath = utils.getFullPathFromResultFileName('gridResults/' + classifierName + '_' + additionalName + '.csv')
    parameterResults.to_csv(resultsPath, sep=',')


def evaluateParameter(classifier, trainData, trainLabels, parameter, parameterOptions):
    parameterGrid = {parameter: parameterOptions}

    grid_search = GridSearchCV(classifier, param_grid=parameterGrid, verbose=1)
    grid_search.fit(trainData, trainLabels)

    resultsDict = grid_search.cv_results_
    resultsDataFrame = pd.DataFrame.from_dict(resultsDict)
    resultsDataFrame.set_index('params', inplace=True)

    return resultsDataFrame


def evaluateParameters(classifier, trainData, trainLabels, parameterGrid):
    print "Running Grid Search"
    grid_search = GridSearchCV(classifier, param_grid=parameterGrid, verbose=1)
    grid_search.fit(trainData, trainLabels)

    resultsDict = grid_search.cv_results_
    resultsDataFrame = pd.DataFrame.from_dict(resultsDict)
    resultsDataFrame.set_index('params', inplace=True)

    return resultsDataFrame


def printReleventResults(results):
    for result in results:
        print ''
        print result['classifierType']
        print 'Train Accuracy: ', result['trainAccuracy']
        print 'Test Accuracy: ', result['testAccuracy']
        print 'Confusion Matrix: '
        print result['confusionMatrix']
        if "RandomForest" in str(result['classifierType']):
            print 'Feature Importance: '
            print result['featureImportance']


def saveResultsFromTrainedClassifier(classifier, classifierName, trainData, trainLabels, testData, testLabels):
    result = {}

    print 'Running classifier: ', str(type(classifier))

    result['classifierType'] = str(type(classifier))

    predictions = classifier.predict(testData)

    trainAccuracy = metrics.accuracy_score(trainLabels, classifier.predict(trainData))
    testAccuracy = metrics.accuracy_score(testLabels, predictions)
    result['trainAccuracy'] = trainAccuracy
    result['testAccuracy'] = testAccuracy

    try:
        confusionMatrix = metrics.confusion_matrix(testLabels, predictions).toList()
        result['confusionMatrix'] = confusionMatrix
    except:
        pass

    try:
        predictProbabilities = classifier.predict_proba(testData)
        logLoss = metrics.log_loss(testLabels, predictProbabilities)
        result['logLoss'] = logLoss
    except:
        pass

    try:
        precision = metrics.precision_score(testLabels, predictions)
        result['precision'] = precision
    except:
        pass

    try:
        recall = metrics.recall_score(testLabels, predictions)
        result['recall'] = recall
    except:
        pass

    try:
        rocAuc = metrics.roc_auc_score(testLabels, predictions)
        result['rocAuc'] = rocAuc
    except:
        pass

    try:
        featureImportanceRaw = zip(trainData, classifier.feature_importances_)
        featureImportance = {}
        for feature, importance in featureImportanceRaw:
            featureImportance[feature] = importance
        result['featureImportance'] = featureImportance
    except:
        pass

    fullPath = utils.getFullPathFromResultFileName(classifierName + '_finalResults' + '.json')
    obj = open(fullPath, 'wb')
    resultsJson = json.dumps(result)
    obj.write(resultsJson)
    obj.close()
