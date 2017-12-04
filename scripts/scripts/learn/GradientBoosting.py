import numpy as np
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor

from scripts.learn import machineLearning
from scripts.learn.machineLearning import tuneNValue

# ______________________________________________________
# HOW LONG WILL MY CLASSIFIER TAKE TO RUN ON MY MACHINE?
# ______________________________________________________
#
# Create a basic classifier
classifier = GradientBoostingRegressor(random_state=43)
classifierName = "GradientBoostingRegressor"  # No spaces, this will be a file name

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
def tuneGradientBoostingNValues():
    nValues = [
        2 ** 4,
        2 ** 5,
        2 ** 6,
        2 ** 7,
        2 ** 8,
        2 ** 9,
        2 ** 10,
        1598,
        2 ** 11,
        2 ** 12,
        2 ** 13,
    ]

    tuneNValue(nValues, classifier, classifierName, jsonFileNames)


# ______________________________________________________
# WHAT ARE THE BEST VALUES OF EACH PARAMETER?
# ______________________________________________________
#
    # This should be a list of all your parameters with a wide range of possible values
def tuneGradientBoostingParametersIndividually(decentNValues):
    parameterGrid = {
        'loss' : ['ls', 'lad', 'huber', 'quantile'],
        'learning_rate' : [.1, .2, .5, 1.0],
        'n_estimators': [50, 100],
        'max_depth' :[1,3,5],
        'max_features': [5, 10],
        'max_leaf_nodes' : [None, 10, 5]
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
def tuneGradientBoostingParameters(decentNValues, parameterGrid):
    parameterGrid = {
    'loss': ['ls', 'lad'],
    'learning_rate': [.1, .01],
    'n_estimators': [50],
    'max_depth': [1],
    'max_features': [10],
    'max_leaf_nodes': [20, 10]
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

    bestParams = machineLearning.tuneParameters(parameterGrid, classifierName, classifier, jsonFileNames, decentNValue)
    return bestParams


# ______________________________________________________
# RUN THE MODEL WITH BEST PARAMETERS
# ______________________________________________________

def runFineTunedGradientBoosting():
    bestRegressor = GradientBoostingRegressor(
        loss='ls',
        learning_rate = .01,
        n_estimators = 50,
        max_depth = 1,
        max_features = 10,
        max_leaf_nodes = 20
    )

    machineLearning.runRegressor(bestRegressor, "GradientBoosting", jsonFileNames)


tuneGradientBoostingNValues()

# Pick a reasonable n value considering you'll be training the model a few hundred times
# We want an n with a high accuracy but low run time
decentNValue = 200
#
# bestParams = tuneGradientBoostingParametersIndividually(decentNValue)
# print ''
# print ''
# print 'here are all possible best parameters'
# print bestParams
# print ''
# print ''
#
# bestParams = tuneGradientBoostingParameters(decentNValue, bestParams)
# print ''
# print ''
# print 'here are actual best parameters'
# print bestParams



runFineTunedGradientBoosting()


