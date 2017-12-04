import numpy as np
from sklearn.ensemble import BaggingRegressor

from scripts.learn import machineLearning
from scripts.learn.machineLearning import tuneNValue

# ______________________________________________________
# HOW LONG WILL MY CLASSIFIER TAKE TO RUN ON MY MACHINE?
# ______________________________________________________
#
# Create a basic classifier
classifier = BaggingRegressor(random_state=43)
classifierName = "BaggingRegressorReddit"  # No spaces, this will be a file name

# Add the names of all data files you want to use to this list
jsonFileNames = [
    'reddit/allRedditComments_weather_sentiment_clean_grouped.json',
]


# We want to see how long it will take to train our classifier
# This will make a file called <classifierName>_number_data_points.csv
def tuneBaggingRegressorNValues():
    nValues = [
        2 ** 4,
        2 ** 5,
        2 ** 6,
        2 ** 7,
        2 ** 8,
        2 ** 9,
        2 ** 10,
        2 ** 11,
        2 ** 12,
        2 ** 13,
        2 ** 14,
        2 ** 15,
    ]

    tuneNValue(nValues, classifier, classifierName, jsonFileNames, dataSource='reddit')


# ______________________________________________________
# WHAT ARE THE BEST VALUES OF EACH PARAMETER?
# ______________________________________________________
#
def tuneBaggingRegressorParametersIndividually(decentNValues):
    # This should be a list of all your parameters with a wide range of possible values
    parameterGrid = {
        'n_estimators': [50, 100],
        'max_samples': [50,100],
        'max_features': [5, 10],
        'bootstrap': [True, False],
        'bootstrap_features': [False, True],
        'warm_start': [False, True],
    }

    threeBestParams = machineLearning.tuneParametersIndividually(parameterGrid, classifierName, classifier,
                                                                 jsonFileNames,
                                                                 decentNValue, 2, dataSource='reddit')
    return threeBestParams


# ______________________________________________________
# WHAT IS THE BEST COMBINATION OF VARIABLES?
# ______________________________________________________
#

# Fill this grid with only the best parameter values, as every single combination will be run
def tuneBaggingRegressorParameters(decentNValues, parameterGrid):
    parameterGrid = {
    'n_estimators': [100],
    'max_samples': [100],
    'max_features': [5],
    'bootstrap': [True],
    'bootstrap_features': [True],
    'warm_start': [True],
    }

    # parameterGrid = {
    #     "n_estimators": [5, 330],
    #     "max_depth": [2, 3],
    #     "min_samples_split": [74, 130],
    #     "min_samples_leaf": [35, 59],
    #     "max_leaf_nodes": [2, 8],
    #     "min_weight_fraction_leaf": [0.2, 0.4],
    #     "max_features": ["auto", "log2"]
    # }

    bestParams = machineLearning.tuneParameters(parameterGrid, classifierName, classifier, jsonFileNames, decentNValue,
                                                dataSource='reddit')
    return bestParams


# ______________________________________________________
# RUN THE MODEL WITH BEST PARAMETERS
# ______________________________________________________
#
def runFineTunedBaggingRegressor():
    bestRegressor = BaggingRegressor(
        n_estimators=100,
        max_samples=100,
        max_features=5,
        bootstrap=True,
        bootstrap_features=True,
        warm_start=True
    )

    machineLearning.runRegressor(bestRegressor, "BaggingRegressorReddit", jsonFileNames, dataSource='reddit')


tuneBaggingRegressorNValues()


# Pick a reasonable n value considering you'll be training the model a few hundred times
# We want an n with a high accuracy but low run time
decentNValue = 10000
#
# bestParams = tuneBaggingRegressorParametersIndividually(decentNValue)
# print ''
# print ''
# print 'here are all possible best parameters'
# print bestParams
# print ''
# print ''
# #
# bestParams = tuneBaggingRegressorParameters(decentNValue, bestParams)
# print ''
# print ''
# print 'here are actual best parameters'
# print bestParams


runFineTunedBaggingRegressor()
