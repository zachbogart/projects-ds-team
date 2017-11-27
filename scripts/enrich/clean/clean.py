import json


class BadDataEntryException(Exception):
    pass


def clean(cityName):
    inputPath = cityName + '_weather_sentiment.json'
    outputPath = cityName + '_weather_sentiment_clean.json'
    with open(inputPath) as data_file:
        dataEntries = json.load(data_file)

        count = 0
        cleanData = []
        for dataEntry in dataEntries:
            if count % 10000 == 0:
                print "Cleaning data -- count: ", count
            count = count + 1

            try:
                dataEntry = removeIncompleteData(dataEntry)
                dataEntry = fixWeatherData(dataEntry)
                dataEntry = removeNeutralSentiment(dataEntry)

                cleanData.append(dataEntry)
            except BadDataEntryException:
                pass

    with open(outputPath, 'w') as outfile:
        json.dump(cleanData, outfile)

    print 'Saved file: ', outputPath


def removeIncompleteData(dataEntry):
    return dataEntry


def fixWeatherData(dataEntry):
    return dataEntry


def removeNeutralSentiment(dataEntry):
    if ('sentiment' not in dataEntry) or (dataEntry['sentiment'] == 0):
        raise BadDataEntryException("No Neutral Sentiment")
    return dataEntry
