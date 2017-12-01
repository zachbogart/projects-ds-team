import numpy as np
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB

from scripts.learn import machineLearning
from scripts.learn.machineLearning import tuneNValue

# ______________________________________________________
# HOW LONG WILL MY CLASSIFIER TAKE TO RUN ON MY MACHINE?
# ______________________________________________________
#
# Create a basic classifier
classifier = GaussianNB()
classifierName = "GaussNB"  # No spaces, this will be a file name

# Add the names of all data files you want to use to this list
jsonFileNames = [
    'chicago_weather_sentiment_clean.json',
    'denver_weather_sentiment_clean.json',
    'detroit_weather_sentiment_clean.json',
    'houston_weather_sentiment_clean.json',
    'manhattan_weather_sentiment_clean.json',
    'phoenix_weather_sentiment_clean.json',
    'sanFrancisco_weather_sentiment_clean.json',
    'seattle_weather_sentiment_clean.json',
]

# We want to see how long it will take to train our classifier
# This will make a file called <classifierName>_number_data_points.csv

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
    2 ** 16,
    2 ** 17,
    2 ** 18,
    2 ** 19,
    2 ** 20,
    2 ** 21,
    2 ** 22,
    2 ** 23,
]

tuneNValue(nValues, classifier, classifierName, jsonFileNames)

# Pick a reasonable n value considering you'll be training the model a few hundred times
# We want an n with a high accuracy but low run time
decentNValue = 30000

# ______________________________________________________
# WHAT ARE THE BEST VALUES OF EACH PARAMETER?
# ______________________________________________________
#

# This should be a list of all your parameters with a wide range of possible values
parameterGrid = {
    # "n_estimators": np.arange(5, 500, 10),
    # "max_depth": np.arange(1, 22, 1),
    # "min_samples_split": np.arange(2, 150, 4),
    # "min_samples_leaf": np.arange(1, 60, 2),
    # "max_leaf_nodes": np.arange(2, 100, 2),
    # "min_weight_fraction_leaf": np.arange(0.1, 0.4, 0.1),
    # "max_features": ["auto", "sqrt", "log2"]
    'priors': [None]
}

machineLearning.tuneParametersIndividually(parameterGrid, classifierName, classifier, jsonFileNames, decentNValue)

# ______________________________________________________
# WHAT IS THE BEST COMBINATION OF VARIABLES?
# ______________________________________________________


# Fill this grid with only the best parameter values, as every single combination will be run
# parameterGrid = {
#     "n_estimators": [5, 220, 330],
#     "max_depth": [1, 2, 3],
#     "min_samples_split": [74, 118, 130],
#     "min_samples_leaf": [35, 57, 59],
#     "max_leaf_nodes": [2, 6, 8],
#     "min_weight_fraction_leaf": [0.2, 0.3, 0.4],
#     "max_features": ["auto", "sqrt", "log2"]
# }

parameterGrid = {
    # "n_estimators": [5, 330],
    # "max_depth": [2, 3],
    # "min_samples_split": [74, 130],
    # "min_samples_leaf": [35, 59],
    # "max_leaf_nodes": [2, 8],
    # "min_weight_fraction_leaf": [0.2, 0.4],
    # "max_features": ["auto", "log2"]
    'priors': [None]
}

machineLearning.tuneParameters(parameterGrid, classifierName, classifier, jsonFileNames, decentNValue)

# ______________________________________________________
# RUN THE MODEL WITH BEST PARAMETERS
# ______________________________________________________
#

bestClassifier = GaussianNB(
    # n_estimators=15,
    # max_depth=2,
    # min_samples_split=120,
    # min_samples_leaf=15,
    # max_leaf_nodes=80,
    # min_weight_fraction_leaf=.2,
    # random_state=0,
    # max_features="auto",
    priors=None
)

machineLearning.runRegressor(bestClassifier, "GaussNB", jsonFileNames)

