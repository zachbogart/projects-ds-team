import json
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor, VotingClassifier, BaggingClassifier, \
    ExtraTreesClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
import timeit

pd.options.mode.chained_assignment = None  # Removes unnecessary warning


def isLabelPositive(label):
    if label > 0:
        return 1
    elif label < 0:
        return 2
    else:
        return 0


def toLabelName(label):
    if label == 2:
        return 'negative'
    elif label == 0:
        return 'neutral'
    else:
        return 'positive'


def doMachineLearning(dataFilePath):
    with open(dataFilePath) as data_file:
        jsonData = json.load(data_file)

    data = pd.DataFrame.from_dict(jsonData, orient='columns')
    data['sentimentScore'] = data['sentiment'].apply(isLabelPositive)
    data['sentimentLabel'] = data['sentimentScore'].apply(toLabelName)

    featureColumnNames = [
        "friends_count",
        "followers",
        "airtemp(C)",
        "dewpoint(C)",
        "windspeed(m/s)",
        "skycoverage(code)",
        "1h-prec(mm)",
        "6h-prec(mm)"
    ]
    labelColumnNames = 'sentimentScore'

    trainPercentage = .75
    trainData, testData, trainLabels, testLabels = train_test_split(data[featureColumnNames], data[labelColumnNames],
                                                                    train_size=trainPercentage)

    print ''
    print('Number of observations in the training data:', len(trainData))
    print('Number of observations in the test data:', len(testData))

    nEstimators = 500
    maxFeatures = "auto"
    criterion = "gini"
    randomForestClassifier = RandomForestClassifier(random_state=0,
                                                    n_estimators=nEstimators,
                                                    max_features=maxFeatures,
                                                    criterion=criterion)
    randomForestClassifier.fit(trainData, trainLabels)

    baggingClassifier = BaggingClassifier()
    baggingClassifier.fit(trainData, trainLabels)

    extraTreesClassifier = ExtraTreesClassifier()
    extraTreesClassifier.fit(trainData, trainLabels)

    results = []

    results.append(runClassifier(randomForestClassifier, testData, testLabels, trainData, trainLabels))
    results.append(runClassifier(baggingClassifier, testData, testLabels, trainData, trainLabels))
    results.append(runClassifier(extraTreesClassifier, testData, testLabels, trainData, trainLabels))

    printReleventResults(results)
    return results


def printReleventResults(results):
    for result in results:
        print ''
        print result['classifierType']
        print 'Train Accuracy: ', result['trainAccuracy']
        print 'Test Accuracy: ', result['testAccuracy']
        print 'Confusion Matrix: '
        print result['confusionMatrix']


def runClassifier(classifier, testData, testLabels, trainData, trainLabels):
    result = {}

    result['classifierType'] = type(classifier)

    predictions = classifier.predict(testData)
    result['predictions'] = predictions

    trainAccuracy = accuracy_score(trainLabels, classifier.predict(trainData))
    testAccuracy = accuracy_score(testLabels, predictions)
    result['trainAccuracy'] = trainAccuracy
    result['testAccuracy'] = testAccuracy

    advancedPredictions = classifier.predict_proba(testData)
    result['advancedPredictions'] = advancedPredictions

    confusionMatrix = confusion_matrix(testLabels, predictions)
    result['confusionMatrix'] = confusionMatrix

    if type(classifier) is RandomForestClassifier:
        featureImportance = list(zip(trainData, classifier.feature_importances_))
        result['featureImportance'] = featureImportance

    return result
