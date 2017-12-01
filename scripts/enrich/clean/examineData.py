import json

import os

import time
import pandas as pd
import numpy as np

from scripts.enrich.clean import clean
from scripts.enrich.weather import augmentWeather
from scripts.enrich.sentiment import sentiment
from scripts.learn.machineLearning import retrieveJsonData
from scripts.utils import utils


def printClassVariables():
    jsonFileNames = [
        'chicago_weather_sentiment_cleaner.json',
        'denver_weather_sentiment_cleaner.json',
        'detroit_weather_sentiment_cleaner.json',
        'houston_weather_sentiment_cleaner.json',
        'manhattan_weather_sentiment_cleaner.json',
        'phoenix_weather_sentiment_cleaner.json',
        'sanFrancisco_weather_sentiment_cleaner.json',
        'seattle_weather_sentiment_cleaner.json',
    ]

    jsonData = retrieveJsonData(jsonFileNames)
    dataframe = pd.DataFrame(jsonData)
    print ''
    print 'icons'
    print dataframe['icon'].unique()

    print ''
    print 'icon counts'
    count = dataframe['icon'].count()
    result = dataframe['icon'].value_counts().div(count)
    print result

    print ''
    print 'precipType'
    print dataframe['precipType'].unique()

    print ''
    print 'precipType counts'
    dataframe = dataframe[['precipType']]
    count = dataframe['precipType'].count()
    result = dataframe['precipType'].value_counts().div(count)

    print result


printClassVariables()
