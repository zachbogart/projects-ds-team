from sklearn.ensemble import RandomForestClassifier

from scripts.machineLearning import train
from scripts.machineLearning.train import tuneNValue
import numpy as np

# ______________________________________________________
# HOW LONG WILL MY CLASSIFIER TAKE TO RUN ON MY MACHINE?
# ______________________________________________________
#
# Create a basic classifier
classifier = RandomForestClassifier()
classifierName = "randomForest"  # No spaces, this will be a file name

# Add the names of all data files you want to use to this list
jsonFileNames = [
    'chicago_weather_sentiment.json',
    'manhattan_weather_sentiment.json',
    'detroit_weather_sentiment.json'
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
]

tuneNValue(nValues, classifier, classifierName, jsonFileNames)

# Pick a reasonable n value considering you'll be training the model a few hundred times
# We want an n with a high accuracy but low run time
decentNValue = 2 ** 13

# ______________________________________________________
# WHAT ARE THE BEST VALUES OF EACH PARAMETER?
# ______________________________________________________
#

# This should be a list of all your parameters with a wide range of possible values
parameterGrid = {
    "n_estimators": np.arange(5, 500, 5),
    "max_depth": np.arange(1, 22, 1),
    "min_samples_split": np.arange(2, 150, 4),
    "min_samples_leaf": np.arange(1, 60, 2),
    "max_leaf_nodes": np.arange(2, 100, 2),
    "min_weight_fraction_leaf": np.arange(0.1, 0.4, 0.1),
    "random_state": np.arange(0, 100, 4),
    "max_features": ["auto", "sqrt", "log2"]
}

train.tuneParametersIndividually(parameterGrid, classifierName, classifier, jsonFileNames, decentNValue)

# ______________________________________________________
# WHAT IS THE BEST COMBINATION OF VARIABLES?
# ______________________________________________________
#

# Fill this grid with only the best parameter values, as every single combination will be run
parameterGrid = {
    "n_estimators": [10, 15, 20],
    "max_depth": [2, 3, 4],
    "min_samples_split": [120, 124, 128],
    "min_samples_leaf": [14, 15, 16],
    "max_leaf_nodes": [80, 82, 84],
    "min_weight_fraction_leaf": [0.1, 0.2, 0.3],
    "random_state": [0, 40, 44],
    "max_features": ["auto", "sqrt", "log2"]
}

train.tuneParameters(parameterGrid, classifierName, classifier, jsonFileNames, decentNValue)

# ______________________________________________________
# RUN THE MODEL WITH BEST PARAMETERS
# ______________________________________________________
#

bestClassifier = RandomForestClassifier(
    n_estimators=15,
    max_depth=2,
    min_samples_split=120,
    min_samples_leaf=15,
    max_leaf_nodes=80,
    min_weight_fraction_leaf=.2,
    random_state=0,
    max_features="auto",
)

train.runClassifier(bestClassifier, "randomForest", jsonFileNames)
