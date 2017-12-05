import json
from time import time

import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split

from scripts.utils import utils

np.random.seed(7)
pd.options.mode.chained_assignment = None  # Removes unnecessary warning

featureColumnNames = [
    'cloudCover',
    # 'summary',
    'temperature',
    'dewPoint',
    # 'followers',
    # 'location',
    # 'location',
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

# labelColumnName = 'sentiment_percent_positive'
labelColumnName = 'sentiment_average'


def tuneParameters(parameterGrid, regressorName, regressor, jsonFileNames, numDataPoints, dataSource='twitter'):
    """
    This function should be called to find the best combination of
    parameters to run. Results will be written as csv file in the form
    <regressorName>_parameterTuning.csv

    Be careful of including too many parameters, this function will
    run EVERY combination of parameters. To find a smaller range of values
    for a parameter try running tuneParametersIndividually first

    :param parameterGrid: ex-- {
        nEstimators: [2,4,6,8],
        maxDepth: [1,10,100,1000]
    }
    :param regressorName: May not contain spaces
    :param regressor:
    :param jsonFileNames: ex-- [
        'chicago_weather_sentiment.json',
        'manhattan_weather_sentiment.json',
        'detroit_weather_sentiment.json'
    ]
    :param numDataPoints: The number of data points we will sample to run this
    """
    if ' ' in regressorName:
        raise Exception('No spaces allowed in regressorName')

    jsonData = retrieveJsonData(jsonFileNames)
    data = pd.DataFrame.from_dict(jsonData, orient='columns')

    usableColumnNames = []
    usableColumnNames.extend(featureColumnNames)
    usableColumnNames.append(labelColumnName)

    finalData = data[usableColumnNames]
    smallerData = randomSampleDatapoints(finalData, numDataPoints)
    trainData = smallerData[featureColumnNames]
    trainLabels = smallerData[labelColumnName]

    numCombinations = computeNumCombinations(parameterGrid)
    print "About to tune parameters with # combinations: ", numCombinations

    results = evaluateParameters(regressor, trainData, trainLabels, parameterGrid)
    bestParams = {}
    bestResult = results.nlargest(1, 'mean_test_score')
    bestResult.index = [0]
    for parameter in parameterGrid:
        value = bestResult['param_' + parameter][0]
        bestParams[parameter] = value
    saveResultsAsCSV(results, regressorName, "parameterTuning", dataSource)
    return bestParams


def tuneParametersIndividually(parameterGrid, regressorName, regressor, jsonFileNames, numDataPoints, numTopParameters,
                               dataSource='twitter'):
    """
    This function will run through each parameter and try every value independent of any
    other variable. The result will be saved in separate files named
    <regressorName>_<parameter>.csv

    :param parameterGrid: ex-- {
        nEstimators: [2,4,6,8],
        maxDepth: [1,10,100,1000]
    }
    :param regressorName: May not contain spaces
    :param regressor:
    :param jsonFileNames: ex-- [
        'chicago_weather_sentiment.json',
        'manhattan_weather_sentiment.json',
        'detroit_weather_sentiment.json'
    ]
    :param numDataPoints: The number of data points we will sample to run this
    :return:
    """
    if ' ' in regressorName:
        raise Exception('No spaces allowed in regressorName')

    jsonData = retrieveJsonData(jsonFileNames)
    data = pd.DataFrame.from_dict(jsonData, orient='columns')

    usableColumnNames = []
    usableColumnNames.extend(featureColumnNames)
    usableColumnNames.append(labelColumnName)

    usableData = data[usableColumnNames].dropna()
    smallerData = randomSampleDatapoints(usableData, numDataPoints)
    trainData = smallerData[featureColumnNames]
    trainLabels = smallerData[labelColumnName]

    bestParams = {}
    for parameter, parameterOptions in dict.items(parameterGrid):
        print ''
        print "Running parameter: ", parameter
        results = evaluateParameter(regressor, trainData, trainLabels, parameter, parameterOptions)
        topRows = results.nlargest(numTopParameters, 'mean_test_score')
        topParams = topRows['param_' + parameter].tolist()
        bestParams[parameter] = topParams
        saveResultsAsCSV(results, regressorName, parameter, dataSource)

    return bestParams


def tuneNValue(nValues, regressor, regressorName, jsonFileNames, dataSource='twitter'):
    """
    This function will run the regressor for every n value and record the
    accuracy and time for each. The result will be saved in a file called
    <regressorName>_number_data_points.csv

    :param nValues: Values of n to run
    :param regressor:
    :param regressorName: May not contain spaces
    :return:
    """
    if ' ' in regressorName:
        raise Exception('No spaces allowed in regressorName')

    jsonData = retrieveJsonData(jsonFileNames)

    data = pd.DataFrame.from_dict(jsonData, orient='columns')

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
        trainPercentage = .8
        trainData, testData, trainLabels, testLabels = train_test_split(sampledData[featureColumnNames],
                                                                        sampledData[labelColumnName],
                                                                        train_size=trainPercentage)
        print ''
        print 'Training n value', nValue

        startTime = time()
        regressor.fit(trainData, trainLabels)
        totalTime = time() - startTime
        predictions = regressor.predict(testData)
        testR2 = metrics.r2_score(testLabels, predictions)
        trainPredictions = regressor.predict(trainData)
        trainR2 = metrics.r2_score(trainLabels, trainPredictions)
        # testAccuracy = metrics.accuracy_score(testLabels, predictions)
        # trainPredictions = regressor.predict(trainData)
        # trainAccuracy = metrics.accuracy_score(trainLabels, trainPredictions)
        results.append({
            'time': totalTime,
            'trainR2': trainR2,
            'testR2': testR2,
        })

    resultsDataFrame = pd.DataFrame(results)
    resultsDataFrame.index = nValues
    saveResultsAsCSV(resultsDataFrame, regressorName, 'number_data_points', dataSource)


def runRegressor(regressor, regressorName, jsonFileNames, numDataPoints=None, dataSource='twitter'):
    """
    This function will run the provided regressor for a specific set of parameters
    Results will be saved to a file called <regressorName>_finalResults.csv

    :param regressorName: May not contain spaces
    :param regressor: Classifier should already be configured with parameters
    :param jsonFileNames:
    :param numDataPoints: Default is None. If not none, will sample the data and use only
                            given number of data points.
    :return:
    """
    if ' ' in regressorName:
        raise Exception('No spaces allowed in regressorName')

    jsonData = retrieveJsonData(jsonFileNames)

    data = pd.DataFrame.from_dict(jsonData, orient='columns')

    usableColumnNames = []
    usableColumnNames.extend(featureColumnNames)
    usableColumnNames.append(labelColumnName)

    finalData = data[usableColumnNames]
    if numDataPoints != None:
        finalData = randomSampleDatapoints(finalData, numDataPoints)

    trainPercentage = .8
    trainData, testData, trainLabels, testLabels = train_test_split(finalData[featureColumnNames],
                                                                    finalData[labelColumnName],
                                                                    train_size=trainPercentage)
    print ''
    print('Number of observations in the training data:', len(trainData))
    print('Number of observations in the test data:', len(testData))

    print "Fitting ", regressorName
    regressor.fit(trainData, trainLabels)

    saveResultsFromTrainedClassifier(regressor, regressorName, trainData, trainLabels, testData, testLabels, dataSource)


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
    if label == -1:
        return 'negative'
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


def saveResultsAsCSV(parameterResults, regressorName, additionalName, dataSource):
    resultsPath = utils.getFullPathFromResultFileName(
        dataSource + '/' + 'gridResults/' + regressorName + '_' + additionalName + '.csv')
    parameterResults.to_csv(resultsPath, sep=',')


def evaluateParameter(regressor, trainData, trainLabels, parameter, parameterOptions):
    parameterGrid = {parameter: parameterOptions}

    grid_search = GridSearchCV(regressor, param_grid=parameterGrid, verbose=1, cv=8)
    grid_search.fit(trainData, trainLabels)

    resultsDict = grid_search.cv_results_
    resultsDataFrame = pd.DataFrame.from_dict(resultsDict)
    resultsDataFrame.set_index('params', inplace=True)

    return resultsDataFrame


def evaluateParameters(regressor, trainData, trainLabels, parameterGrid):
    print "Running Grid Search"
    grid_search = GridSearchCV(regressor, param_grid=parameterGrid, verbose=1, cv=8)
    grid_search.fit(trainData, trainLabels)

    resultsDict = grid_search.cv_results_
    resultsDataFrame = pd.DataFrame.from_dict(resultsDict)
    resultsDataFrame.set_index('params', inplace=True)

    return resultsDataFrame


def printReleventResults(results):
    for result in results:
        print ''
        print result['regressorType']
        print 'Train Accuracy: ', result['trainAccuracy']
        print 'Test Accuracy: ', result['testAccuracy']
        print 'Confusion Matrix: '
        print result['confusionMatrix']
        if "RandomForest" in str(result['regressorType']):
            print 'Feature Importance: '
            print result['featureImportance']


def saveResultsFromTrainedClassifier(regressor, regressorName, trainData, trainLabels, testData, testLabels,
                                     dataSource):
    result = {}

    print 'Running regressor: ', str(type(regressor))

    result['regressorType'] = str(type(regressor))

    predictions = regressor.predict(testData)
    trainPredictions = regressor.predict(trainData)
    result['actualVsPrediction'] = zip(testLabels, predictions.tolist())

    # trainAccuracy = metrics.accuracy_score(trainLabels, regressor.predict(trainData))
    # testAccuracy = metrics.accuracy_score(testLabels, predictions)
    # result['trainAccuracy'] = trainAccuracy
    # result['testAccuracy'] = testAccuracy
    testExplained_variance = metrics.explained_variance_score(testLabels, predictions)
    testNeg_mean_absolute_error = metrics.mean_absolute_error(testLabels, predictions)
    testNeg_mean_squared_error = metrics.mean_squared_error(testLabels, predictions)
    testNeg_median_absolute_error = metrics.median_absolute_error(testLabels, predictions)
    testR2 = metrics.r2_score(testLabels, predictions)
    result['testExplained_variance'] = testExplained_variance
    result['testNeg_mean_absolute_error'] = testNeg_mean_absolute_error
    result['testNeg_mean_squared_error'] = testNeg_mean_squared_error
    result['testNeg_median_absolute_error'] = testNeg_median_absolute_error
    result['testR2'] = testR2

    trainExplained_variance = metrics.explained_variance_score(trainLabels, trainPredictions)
    trainNeg_mean_absolute_error = metrics.mean_absolute_error(trainLabels, trainPredictions)
    trainNeg_mean_squared_error = metrics.mean_squared_error(trainLabels, trainPredictions)
    trainNeg_median_absolute_error = metrics.median_absolute_error(trainLabels, trainPredictions)
    trainR2 = metrics.r2_score(trainLabels, trainPredictions)
    result['trainExplained_variance'] = trainExplained_variance
    result['trainNeg_mean_absolute_error'] = trainNeg_mean_absolute_error
    result['trainNeg_mean_squared_error'] = trainNeg_mean_squared_error
    result['trainNeg_median_absolute_error'] = trainNeg_median_absolute_error
    result['trainR2'] = trainR2

    # try:
    #     predictProbabilities = regressor.predict_proba(testData)
    #     logLoss = metrics.log_loss(testLabels, predictProbabilities)
    #     result['logLoss'] = logLoss
    # except:
    #     pass
    #
    # try:
    #     precision = metrics.precision_score(testLabels, predictions)
    #     result['precision'] = precision
    # except:
    #     pass
    #
    # try:
    #     recall = metrics.recall_score(testLabels, predictions)
    #     result['recall'] = recall
    # except:
    #     pass
    #
    # try:
    #     rocAuc = metrics.roc_auc_score(testLabels, predictions)
    #     result['rocAuc'] = rocAuc
    # except:
    #     pass
    #
    # try:
    #     confusionMatrix = metrics.confusion_matrix(testLabels, predictions)
    #     result['confusionMatrix'] = confusionMatrix.tolist()
    # except:
    #     pass

    try:
        featureImportanceRaw = zip(trainData, regressor.feature_importances_)
        featureImportance = {}
        for feature, importance in featureImportanceRaw:
            featureImportance[feature] = importance
        result['featureImportance'] = featureImportance
    except:
        pass

    fullPath = utils.getFullPathFromResultFileName(dataSource + '/' + regressorName + '_finalResults' + '.json')
    obj = open(fullPath, 'wb')
    resultsJson = json.dumps(result)
    obj.write(resultsJson)
    obj.close()
