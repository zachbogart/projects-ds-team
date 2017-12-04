import numpy as np
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB

from scripts.learn import machineLearning
from scripts.learn.machineLearning import tuneNValue


# class sklearn.ensemble.
# BaggingRegressor(base_estimator=None, n_estimators=10, max_samples=1.0, max_features=1.0, bootstrap=True, bootstrap_features=False, oob_score=False, warm_start=False, n_jobs=1, random_state=None, verbose=0)[source]


# ______________________________________________________
# HOW LONG WILL MY CLASSIFIER TAKE TO RUN ON MY MACHINE?
# ______________________________________________________
#
# Create a basic classifier
classifier = BaggingClassifier()
classifierName = "BaggingClassifier"  # No spaces, this will be a file name

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
# parameterGrid = {
#     'n_estimators': [50, 100],
#     'max_samples': [100,1000,10000],
#     'max_features': [5, 10],
#     'bootstrap': [True, False],
#     'bootstrap_features': [False, True],
#     'warm_start': [False, True],
# }
#
# machineLearning.tuneParametersIndividually(parameterGrid, classifierName, classifier, jsonFileNames, decentNValue)
# #
# # ______________________________________________________
# # WHAT IS THE BEST COMBINATION OF VARIABLES?
# # ______________________________________________________
#
#
# # Fill this grid with only the best parameter values, as every single combination will be run
#
# parameterGrid = {
#     'base_estimator': [None],
#     'n_estimators': [50,100],
#     'max_samples': [1000, 10000],
#     'max_features': [5],
#     'bootstrap': [True],
#     'bootstrap_features': [True],
#     'oob_score': [False],
#     'warm_start': [True],
#     'n_jobs': [-1],
#     'random_state': [0],
#     'verbose': [1]
# }
# #
# machineLearning.tuneParameters(parameterGrid, classifierName, classifier, jsonFileNames, decentNValue)
#
# # ______________________________________________________
# # RUN THE MODEL WITH BEST PARAMETERS
# # ______________________________________________________
# #
#
bestClassifier = BaggingClassifier(
    base_estimator= None,
    n_estimators=50,
    max_samples=1000,
    max_features=5,
    bootstrap=True,
    bootstrap_features= True,
    oob_score=False,
    warm_start=True,
    n_jobs= -1,
    random_state=0,
    verbose=1
    )
#
machineLearning.runRegressor(bestClassifier, "BaggingClassifier", jsonFileNames)
#
