from sklearn.ensemble import RandomForestClassifier
import numpy as np
from time import time

from scripts.machineLearning import train

classifier = RandomForestClassifier()

jsonFileNames = [
    'chicago_weather_sentiment.json',
    'manhattan_weather_sentiment.json',
    'detroit_weather_sentiment.json'
]

parameterGrid = {
    "n_estimators": np.arange(5, 20, 5),
    # "n_estimators": np.arange(5, 500, 90),
    # "max_depth": np.arange(1, 22, 4),
    # "min_samples_split": np.arange(2, 150, 10),
    # "min_samples_leaf": np.arange(1, 60, 5),
    # "max_leaf_nodes": np.arange(2, 100, 4),
    # "min_weight_fraction_leaf": np.arange(0.1, 0.4, 0.1),
    # "random_state": np.arange(0, 100, 25),
    "max_features": ["auto", "sqrt", "log2"]
}



startTime = time()
train.tuneParameters(parameterGrid, "randomForest", classifier, jsonFileNames, 100000)
print 'Total Time: ', time() - startTime

# Tune individually to find best grid

# parameterGridIndividually = {
#     "n_estimators": np.arange(5, 500, 10),
#     "max_depth": np.arange(1, 22, 2),
#     "min_samples_split": np.arange(2, 150, 4),
#     "min_samples_leaf": np.arange(1, 60, 1),
#     "max_leaf_nodes": np.arange(2, 100, 2),
#     "min_weight_fraction_leaf": np.arange(0.1, 0.4, 0.1),
#     "random_state": np.arange(0, 100, 4),
#     "max_features": ["auto", "sqrt", "log2"]
# }
#
# startTime = time()
# train.tuneParametersIndividually(parameterGridIndividually, "randomForest", classifier, jsonFileNames, 100000)
# print 'Total Time: ', time() - startTime
