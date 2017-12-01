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

            if hasCompleteData(dataEntry) and hasNonNegativeSentiment(dataEntry):
                dataEntry = fixWeatherData(dataEntry)
                cleanData.append(dataEntry)

    with open(outputPath, 'w') as outfile:
        json.dump(cleanData, outfile)

    print 'Saved file: ', outputPath


def hasCompleteData(dataEntry):
    # TODO: Code this
    return True


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
                u'partly-cloudy-night': .3, 'wind': .5, 'rain': .9}

    if 'cloudCover' not in dataEntry:
        dataEntry['cloudCover'] = iconDict[dataEntry['icon']]

    return dataEntry


def hasNonNegativeSentiment(dataEntry):
    if ('sentiment' not in dataEntry) or (dataEntry['sentiment'] == 0):
        return False
    return True
