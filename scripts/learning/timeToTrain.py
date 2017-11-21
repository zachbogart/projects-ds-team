from sklearn.ensemble import RandomForestClassifier
import numpy as np
from time import time

from scripts.machineLearning.train import tuneNValue

classifier = RandomForestClassifier()

jsonFileNames = [
        'chicago_weather_sentiment.json',
        'manhattan_weather_sentiment.json',
        'detroit_weather_sentiment.json'
    ]

nValues = [
    2**4,
    2**5,
    2**6,
    2**7,
    2**8,
    2**9,
    2**10,
    2**11,
    2**12,
    2**13,
    2**14,
    2**15,
    2**16,
    2**17,
    2**18,
    2**19,
    2**20,
]

startTime = time()
tuneNValue(nValues, classifier, "randomForest")
print 'Total Time: ', time() - startTime
