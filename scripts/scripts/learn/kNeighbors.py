import numpy as np
from sklearn.neighbors import KNeighborsRegressor

from scripts.learn import machineLearning
from scripts.learn.machineLearning import tuneNValue

# ______________________________________________________
# HOW LONG WILL MY CLASSIFIER TAKE TO RUN ON MY MACHINE?
# ______________________________________________________
#
# Create a basic classifier
classifier = KNeighborsRegressor()
classifierName = "KNeighbors"  # No spaces, this will be a file name

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
def tuneKNeighborsNValues():
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
def tuneKNeighborsParametersIndividually(decentNValues):
    # This should be a list of all your parameters with a wide range of possible values
    parameterGrid = {
        "n_neighbors": np.arange(5, 100, 5),
        "leaf_size": np.arange(1, 100, 5),
        "weights": ['uniform', 'distance'],
        "algorithm": ['ball_tree', 'kd_tree', 'brute'],
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
def tuneKNeighborsParameters(decentNValues, parameterGrid):
    parameterGrid = {
        "n_neighbors": [65,70],
        "leaf_size": [46,51],
        "weights": ['uniform', 'distance'],
        "algorithm": ['kd_tree', 'brute'],
    }

    bestParams = machineLearning.tuneParameters(parameterGrid, classifierName, classifier, jsonFileNames, decentNValue)
    return bestParams


# ______________________________________________________
# RUN THE MODEL WITH BEST PARAMETERS
# ______________________________________________________
#
def runFineTunedKNeighbors():
    bestRegressor = KNeighborsRegressor(
        n_neighbors=65,
        leaf_size=46,
        weights='uniform',
        algorithm='kd_tree',
    )

    machineLearning.runRegressor(bestRegressor, "kNeighborsTwitter", jsonFileNames)


# tuneKNeighborsNValues()

# Pick a reasonable n value considering you'll be training the model a few hundred times
# We want an n with a high accuracy but low run time
decentNValue = 1598

bestParams = tuneKNeighborsParametersIndividually(decentNValue)
print ''
print ''
print 'here are all possible best parameters'
print bestParams
print ''
print ''

bestParams = tuneKNeighborsParameters(decentNValue, bestParams)
print ''
print ''
print 'here are actual best parameters'
print bestParams


runFineTunedKNeighbors()
