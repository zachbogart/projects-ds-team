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
    # TODO: Code this
    return dataEntry


def hasNonNegativeSentiment(dataEntry):
    if ('sentiment' not in dataEntry) or (dataEntry['sentiment'] == 0):
        return False
    return True
