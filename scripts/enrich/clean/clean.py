import json

from scripts.utils import utils


def clean(cityName):
    inputPath = utils.getFullPathFromDataFileName(cityName + '_weather_sentiment.json')
    outputPath = utils.getFullPathFromDataFileName(cityName + '_weather_sentiment_clean.json')
    with open(inputPath) as data_file:
        dataEntries = json.load(data_file)

        count = 0
        cleanData = []
        for dataEntry in dataEntries:
            if count % 100000 == 0:
                print "Cleaning data -- count: ", count
            count = count + 1

            if hasNonNegativeSentiment(dataEntry) and hasWeatherData(dataEntry):
                addCreatedField(dataEntry)
                fixWeatherData(dataEntry)
                addSentimentLabel(dataEntry)
                cleanData.append(dataEntry)

    print 'Saving file: ', outputPath
    with open(outputPath, 'w') as outfile:
        json.dump(cleanData, outfile)
    print 'Saved file: ', outputPath


def isLabelPositive(label):
    if label > 0:
        return 1
    elif label < 0:
        return 0
    else:
        raise Exception("The sentiment should not be 0. Neutral data should have been removed")


def addSentimentLabel(dataEntry):
    dataEntry['sentimentScore'] = isLabelPositive(dataEntry['sentiment'])
    # return dataEntry

def hasWeatherData(dataEntry):
    return 'temperature' in dataEntry

def addCreatedField(dataEntry):
    if 'created' in dataEntry: # Reddit Data
        dataEntry['created'] = int(dataEntry['created'])
    else: # Twitter data
        dataEntry['created'] = int(dataEntry['created_at']['$date'] / 1e3)
    # return dataEntry


def fixWeatherData(dataEntry):
    # precipType: set value to 'NoPrecip'
    if 'precipType' not in dataEntry:
        dataEntry['precipType'] = 'NoPrecip'

    dataEntry['precipTypeNone'] = dataEntry['precipType'] == 'NoPrecip'
    dataEntry['precipTypeRain'] = dataEntry['precipType'] == 'rain'
    dataEntry['precipTypeSnow'] = dataEntry['precipType'] == 'snow'

    # remove ozone, windGusts and uv index from the dataframe
    try:
        del dataEntry['ozone']
    except KeyError:
        pass
    try:
        del dataEntry['uvIndex']
    except KeyError:
        pass
    try:
        del dataEntry['windGust']
    except KeyError:
        pass

        # handle cloudCover
    iconDict = {'fog': .7, 'clear-night': 0, 'clear-day': 0, 'partly-cloudy-day': .3, 'cloudy': .5,
                'partly-cloudy-night': .3, 'wind': .5, 'rain': .9, 'snow': 1}

    if 'cloudCover' not in dataEntry:
        dataEntry['cloudCover'] = iconDict[dataEntry['icon']]

    # return dataEntry


def hasNonNegativeSentiment(dataEntry):
    if ('sentiment' not in dataEntry) or (dataEntry['sentiment'] == 0):
        return False
    return True
