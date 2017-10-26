# -*- coding: utf-8 -*-

import tweepy
from pymongo import MongoClient
from textwrap import TextWrapper
from tweepy.utils import import_simplejson
import datetime
import jsonpickle

json = import_simplejson()

auth1 = tweepy.auth.OAuthHandler('eOihmPsLf6q0ro03OFyDExyaH', 'XfOAN3SYME0vCRaaUqCsbbxUxNR88JdRKjLswqyGuZZ7fdfeB3')
auth1.set_access_token('2847047537-wwYPjhsb78FltOxFk8nFvvCtWD6zCVs9JE9qghh',
                       '4fjuf9awSDlNT3AsU7FZFu9AzQcIysKfX0b5IOetxkBr7')
api = tweepy.API(auth1)

class StreamListener(tweepy.StreamListener):
    print 'About to connect to Mongo'
    mongo = MongoClient('localhost', 27017)
    mongo_db = mongo['twitterData']
    mongo_collection = mongo_db['theseAreTweets']
    print 'Connection made to:'
    print 'db name: ' + mongo_db.name
    print 'collection name: ' + mongo_collection.name

    status_wrapper = TextWrapper(width=140, initial_indent='', subsequent_indent='')
    numTweets = 2
    placeName = "Manhattan"

    def setMongoCollection(self, mongoCollectionName):
        print mongoCollectionName
        self.mongo_collection = self.mongo_db[mongoCollectionName]

    def setPlaceName(self, placeName):
        self.placeName = placeName

    def setNumTweets(self, numTweets):
        self.numTweets = numTweets

    def on_status(self, status):
        tempA = self.status_wrapper.fill(status.text)
        tempB = status.retweeted
        tempC = status.user.lang
        tempD = status.geo
        count = 0
        if status.place is not None:
            print status.place.name
        if status.place is not None and status.place.name == self.placeName and (
                    (('en' in tempC) and (tempB is False)) and (not ('RT') in tempA[:2]) and (
                        ((('http' or 'www') in tempA) and ((' ') in tempA)) or (
                            not ('http' or 'www') in tempA)) and tempA is not None):
            try:
                body = self.status_wrapper.fill(status.text)
                place = status.place.name
                print ''
                print ''
                print body
                print ''
                print place
                print ''
                self.mongo_collection.insert({
                    'body': body,
                    'followers': status.user.followers_count,
                    'screen_name': status.author.screen_name,
                    'friends_count': status.user.friends_count,
                    'created_at': status.created_at,
                    'message_id': status.id,
                    'location': place,
                    'local_datetime': datetime.datetime.now()
                })
                count = self.mongo_collection.count()
                print 'tweets saved: %s', count
            except Exception, (e):
                print('Exception reached: ' + str(e))
                pass
            if count >= self.numTweets:
                raise Exception("Ending stream")


def saveTweets(numTweets, mongoCollectionName, locationCoordinates, locationName):
    try:
        l = StreamListener()
        l.setPlaceName(locationName)
        l.setNumTweets(numTweets)
        l.setMongoCollection(mongoCollectionName)
        streamer = tweepy.Stream(auth=auth1, listener=l, timeout=3000)
        place_id = '01a9a39529b27f36'

        streamer.filter(locations=locationCoordinates)
        # streamer.filter(None, "q=place:%s" % place_id)
        # streamer.filter(None, "place:%s" % place_id)
        # streamer.filter(None, "place:%s" % place_id)
        # streamer.filter(None, searchTerms)
    except Exception, (e):
        print str(e)


def getPlaceID(placeName):
    places = api.geo_search(query=placeName, granularity="city")
    place_id = places[0].id
    print places
    print place_id
    print places[0].bounding_box.coordinates
    # New York, NY == 27485069891a7938
    # Manhattan == 01a9a39529b27f36


def getNYCTweets():
    place_id = '01a9a39529b27f36'
    tweets = api.search(q="place:%s" % place_id, count=100)
    print "We found %s tweets" % str(len(tweets))
    # for tweet in tweets:
    #     print tweet.text + " | " + tweet.place.name if tweet.place else "Undefined place"


# def getTweetsAndSaveToJson():
#     tweetCount = 0
#     searchQuery = "*"
#     maxTweets = 10
#
#     # Open a text file to save the tweets to
#     with open('../data/manhattan2.json', 'wb') as f:
#
#         # Tell the Cursor method that we want to use the Search API (api.search)
#         # Also tell Cursor our query, and the maximum number of tweets to return
#         for tweet in tweepy.Cursor(api.search, q=searchQuery).items(maxTweets):
#
#             # Verify the tweet has place info before writing (It should, if it got past our place filter)
#             if tweet.place is not None:
#                 # Write the JSON format to the text file, and add one to the number of tweets we've collected
#                 f.write(jsonpickle.encode(tweet._json, unpicklable=False) + '\n')
#                 tweetCount += 1
#
#         # Display how many tweets we have collected
#         print("Downloaded {0} tweets".format(tweetCount))
