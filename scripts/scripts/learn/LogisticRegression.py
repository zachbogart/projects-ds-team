from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from scripts.learn import machineLearning
import numpy as np
import os
import pandas as pd

os.chdir('/Users/michelkauffmann/desktop/Columbia Files/Projects in Data Science/Homework/Project/projects-ds-team-master/data/')

# ______________________________________________________
# HOW LONG WILL MY CLASSIFIER TAKE TO RUN ON MY MACHINE?
# ______________________________________________________
#
# Create a basic classifier
classifier = LogisticRegression()
classifierName = "logisticRegression"  # No spaces, this will be a file name

# Add the names of all data files you want to use to this list
jsonFileNames = [
    'chicago_weather_sentiment_clean.json',
    'manhattan_weather_sentiment_clean.json',
    'detroit_weather_sentiment_clean.json',
    'phoenix_weather_sentiment_clean.json',
    'sanFrancisco_weather_sentiment_clean.json',
    'seattle_weather_sentiment_clean.json',
    'houston_weather_sentiment_clean.json',
    'denver_weather_sentiment_clean.json' 
]

city = pd.read_json('detroit_weather_sentiment_clean.json')

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

machineLearning.tuneNValue(nValues, classifier, classifierName, jsonFileNames)

# Pick a reasonable n value considering you'll be training the model a few hundred times
# We want an n with a high accuracy but low run time
decentNValue = 2 ** 15

# ______________________________________________________
# WHAT ARE THE BEST VALUES OF EACH PARAMETER?
# ______________________________________________________
#

# This should be a list of all your parameters with a wide range of possible values
parameterGrid = {
    "C" : [0.001, 0.01, 0.1, 1, 10, 100, 1000],
    "fit_intercept": [True, False],
    "solver": ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga'],
    "verbose": np.arange(0, 100, 4),
    "warm_start": [True, False],
    "random_state": np.arange(0, 100, 4)
}

machineLearning.tuneParametersIndividually(parameterGrid, classifierName, classifier, jsonFileNames, decentNValue)

# ______________________________________________________
# WHAT IS THE BEST COMBINATION OF VARIABLES?
# ______________________________________________________
#

# Fill this grid with only the best parameter values, as every single combination will be run
parameterGrid = {
    "C" : [1000, 0.01, 10],
    "fit_intercept": [False],
    "solver": ['lbfgs', 'liblinear'],
    "verbose": [56, 68, 84, 24],
    "warm_start": [False],
    "random_state": [92, 12, 20, 56]
}

machineLearning.tuneParameters(parameterGrid, classifierName, classifier, jsonFileNames, decentNValue)

# ______________________________________________________
# RUN THE MODEL WITH BEST PARAMETERS
# ______________________________________________________
#

bestClassifier = LogisticRegression(
    C = 0.01,
    fit_intercept = False,
    solver = 'lbfgs',
    verbose = 84,
    warm_start = False,
    random_state = 92
)

machineLearning.runRegressor(bestClassifier, "LogisticRegression", jsonFileNames)
