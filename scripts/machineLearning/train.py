import json
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
pd.options.mode.chained_assignment = None #Removes unnecessary warning

def doMachineLearning(dataFilePath):
    with open(dataFilePath) as data_file:
        jsonData = json.load(data_file)

    data = pd.DataFrame.from_dict(jsonData, orient='columns')

    data['is_train'] = np.random.uniform(0, 1, len(data)) <= .75

    trainingData, testingData = data[data['is_train'] == True], data[data['is_train'] == False]

    print('Number of observations in the training data:', len(trainingData))
    print('Number of observations in the test data:', len(testingData))

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
    features = trainingData[featureColumnNames]


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


    trainingData['sentimentScore'] = trainingData['sentiment'].apply(isLabelPositive)
    testingData['sentimentScore'] = testingData['sentiment'].apply(isLabelPositive)
    testingData['sentimentLabel'] = testingData['sentimentScore'].apply(toLabelName)

    randomForestClassifier = RandomForestClassifier(random_state=0)
    randomForestClassifier.fit(features, trainingData['sentimentScore'])

    predictions = randomForestClassifier.predict(testingData[featureColumnNames])
    print ''
    print 'predictions: '
    print predictions

    advancedPredictions = randomForestClassifier.predict_proba(testingData[featureColumnNames])
    print ''
    print 'advanced predictions: '
    print advancedPredictions

    namedPredictions = map(toLabelName, predictions)
    print ''
    print 'named predictions: '
    print namedPredictions

    confusionMatrix = pd.crosstab(testingData['sentimentLabel'], np.array(namedPredictions), rownames=['Actual'],
                                  colnames=['Predicted'])
    print ''
    print 'confusionMatrix: '
    print confusionMatrix

    featureImportance = list(zip(trainingData[featureColumnNames], randomForestClassifier.feature_importances_))
    print ''
    print 'featureImportance: '
    print featureImportance
