import json
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
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

    randomForestClassifier = RandomForestClassifier(random_state=0)
    randomForestClassifier.fit(trainData, trainLabels)

    predictions = randomForestClassifier.predict(testData)
    print ''
    print 'predictions: '
    print predictions

    trainAccuracy = accuracy_score(trainLabels, randomForestClassifier.predict(trainData))
    testAccuracy = accuracy_score(testLabels, predictions)
    print ''
    print "Train Accuracy: ", trainAccuracy
    print "Test Accuracy: ", testAccuracy

    advancedPredictions = randomForestClassifier.predict_proba(testData)
    print ''
    print 'advanced predictions: '
    print advancedPredictions

    confusionMatrix = confusion_matrix(testLabels, predictions)
    print ''
    print 'confusionMatrix: '
    print confusionMatrix

    featureImportance = list(zip(trainData, randomForestClassifier.feature_importances_))
    print ''
    print 'featureImportance: '
    print featureImportance

    return confusionMatrix
