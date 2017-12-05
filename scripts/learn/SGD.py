import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import SGDRegressor
from scripts.learn import machineLearning
from scripts.learn.machineLearning import tuneNValue

# ______________________________________________________
# HOW LONG WILL MY CLASSIFIER TAKE TO RUN ON MY MACHINE?
# ______________________________________________________
#
# Create a basic classifier
regressor = SGDRegressor(random_state = 15)
regressorName = "StochasticGradientDescent"  # No spaces, this will be a file name

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
def tuneSGDNValues():
    nValues = [
        2 ** 4,
        2 ** 5,
        2 ** 6,
        2 ** 7,
        2 ** 8,
        2 ** 9,
        2 ** 10,
        1599,
        2 ** 11,
        2 ** 12,
        2 ** 13,
    ]

    tuneNValue(nValues, regressor, regressorName, jsonFileNames)


# ______________________________________________________
# WHAT ARE THE BEST VALUES OF EACH PARAMETER?
# ______________________________________________________
#
def tuneSGDParametersIndividually(decentNValues):
    # This should be a list of all your parameters with a wide range of possible values
    parameterGrid = {
        "loss" : ['squared_loss', 'huber', 'epsilon_insensitive', 'squared_epsilon_insensitive'],
        "penalty": ['none', 'l2', 'l1', 'elasticnet'],
        "alpha": np.arange(0.00001, 100, 10),
        "l1_ratio": np.arange(0, 1, 0.1),
        "fit_intercept": [True, False],
        "shuffle": [True, False],
        "epsilon": np.arange(0.00001, 100, 10),
        "learning_rate": ['constant', 'optimal', 'invscaling']
    }

    threeBestParams = machineLearning.tuneParametersIndividually(parameterGrid, regressorName, regressor,
                                                                 jsonFileNames,
                                                                 decentNValue, 2)
    return threeBestParams


# ______________________________________________________
# WHAT IS THE BEST COMBINATION OF VARIABLES?
# ______________________________________________________
#

# Fill this grid with only the best parameter values, as every single combination will be run
def tuneSGDParameters(decentNValues, parameterGrid):
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

    bestParams = machineLearning.tuneParameters(parameterGrid, regressorName, regressor, jsonFileNames, decentNValue)
    return bestParams


# ______________________________________________________
# RUN THE MODEL WITH BEST PARAMETERS
# ______________________________________________________
#
def runFineTunedSGD():
    bestRegressor = SGDRegressor(
        loss = 'huber',
        penalty = 'l1',
        alpha = 20.00001,
        l1_ratio = 0.40000000000000002,
        fit_intercept = True,
        shuffle = True,
        epsilon = 30.0001,
        learning_rate = 'invscaling'
    )

    machineLearning.runRegressor(bestRegressor, "SGD", jsonFileNames)


# tuneSGDNValues()

# Pick a reasonable n value considering you'll be training the model a few hundred times
# We want an n with a high accuracy but low run time
decentNValue = 2000

bestParams = tuneSGDParametersIndividually(decentNValue)
print ''
print ''
print 'here are all possible best parameters'
print bestParams
print ''
print ''

bestParams = tuneSGDParameters(decentNValue, bestParams)
print ''
print ''
print 'here are actual best parameters'
print bestParams

runFineTunedSGD()
