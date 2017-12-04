import numpy as np
from sklearn.ensemble import RandomForestRegressor

from scripts.learn import machineLearning
from scripts.learn.machineLearning import tuneNValue

# ______________________________________________________
# HOW LONG WILL MY CLASSIFIER TAKE TO RUN ON MY MACHINE?
# ______________________________________________________
#
# Create a basic classifier
classifier = RandomForestRegressor(random_state=43)
classifierName = "randomForest"  # No spaces, this will be a file name

# Add the names of all data files you want to use to this list
jsonFileNames = [
    'chicago_weather_sentiment_clean_grouped.json',
    'denver_weather_sentiment_clean_grouped.json',
    'detroit_weather_sentiment_clean_grouped.json',
    'houston_weather_sentiment_clean_grouped.json',
    'manhattan_weather_sentiment_clean_grouped.json',
    'phoenix_weather_sentiment_clean_grouped.json',
    'sanFrancisco_weather_sentiment_clean_grouped.json',
    'seattle_weather_sentiment_clean_grouped.json',
]


# We want to see how long it will take to train our classifier
# This will make a file called <classifierName>_number_data_points.csv
def tuneRandomForestNValues():
    nValues = [
        2 ** 4,
        2 ** 5,
        2 ** 6,
        2 ** 7,
        2 ** 8,
        2 ** 9,
        2 ** 10,
        1500,
        1600,
        1700,
        1800,
        2 ** 11,
        2 ** 12,
        2 ** 13,
    ]

    tuneNValue(nValues, classifier, classifierName, jsonFileNames)


# ______________________________________________________
# WHAT ARE THE BEST VALUES OF EACH PARAMETER?
# ______________________________________________________
#
def tuneRandomForestParametersIndividually(decentNValues):
    # This should be a list of all your parameters with a wide range of possible values
    parameterGrid = {
        "n_estimators": np.arange(10, 500, 40),
        "max_depth": np.arange(1, 14, 1),
        "min_samples_split": np.arange(2, 203, 10),
        "min_samples_leaf": np.arange(1, 81, 4),
        "max_leaf_nodes": np.arange(2, 20, 1),
        "min_weight_fraction_leaf": np.arange(0.1, 0.4, 0.1),
        "max_features": ["auto", "sqrt", "log2"]
    }

    threeBestParams = machineLearning.tuneParametersIndividually(parameterGrid, classifierName, classifier,
                                                                 jsonFileNames,
                                                                 decentNValue, 2)
    return threeBestParams


# ______________________________________________________
# WHAT IS THE BEST COMBINATION OF VARIABLES?
# ______________________________________________________
#

# Fill this grid with only the best parameter values, as every single combination will be run
def tuneRandomForestParameters(decentNValues, parameterGrid):
    # parameterGrid = {
    #     "n_estimators": [20, 35, 110],
    #     "max_depth": [3, 4, 2],
    #     "min_samples_split": [130, 66, 42],
    #     "min_samples_leaf": [59, 47, 53],
    #     "max_leaf_nodes": [18, 20, 4],
    #     "min_weight_fraction_leaf": [0.2, 0.1, 0.4],
    #     "max_features": ["auto", "sqrt", "log2"]
    # }

    # parameterGrid = {
    #     "n_estimators": [5, 330],
    #     "max_depth": [2, 3],
    #     "min_samples_split": [74, 130],
    #     "min_samples_leaf": [35, 59],
    #     "max_leaf_nodes": [2, 8],
    #     "min_weight_fraction_leaf": [0.2, 0.4],
    #     "max_features": ["auto", "log2"]
    # }

    bestParams = machineLearning.tuneParameters(parameterGrid, classifierName, classifier, jsonFileNames, decentNValue)
    return bestParams


# ______________________________________________________
# RUN THE MODEL WITH BEST PARAMETERS
# ______________________________________________________
#
def runFineTunedRandomForest():
    bestRegressor = RandomForestRegressor(
        n_estimators=20,
        max_depth=2,
        min_samples_split=42,
        min_samples_leaf=47,
        max_leaf_nodes=4,
        min_weight_fraction_leaf=.2,
        max_features="auto",
        random_state=43,
    )

    machineLearning.runRegressor(bestRegressor, "randomForest", jsonFileNames)


tuneRandomForestNValues()

# Pick a reasonable n value considering you'll be training the model a few hundred times
# We want an n with a high accuracy but low run time
decentNValue = 1598

# bestParams = tuneRandomForestParametersIndividually(decentNValue)
# print ''
# print ''
# print 'here are all possible best parameters'
# print bestParams
# print ''
# print ''
#
# bestParams = tuneRandomForestParameters(decentNValue, bestParams)
# print ''
# print ''
# print 'here are actual best parameters'
# print bestParams


# runFineTunedRandomForest()
