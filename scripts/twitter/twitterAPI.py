# -*- coding: utf-8 -*-

import tweepy
from pymongo import MongoClient
from textwrap import TextWrapper
from tweepy.utils import import_simplejson
import datetime

json = import_simplejson()

auth1 = tweepy.auth.OAuthHandler('eOihmPsLf6q0ro03OFyDExyaH', 'XfOAN3SYME0vCRaaUqCsbbxUxNR88JdRKjLswqyGuZZ7fdfeB3')
auth1.set_access_token('2847047537-wwYPjhsb78FltOxFk8nFvvCtWD6zCVs9JE9qghh',
                       '4fjuf9awSDlNT3AsU7FZFu9AzQcIysKfX0b5IOetxkBr7')
api = tweepy.API(auth1)

#auth2 = tweepy.auth.OAuthHandler('POovwpxYttFBaFA4HsvUCuu3E','dV0F0xu0q1TdeqBam7hydeZ6uo77NpY9Rh4hp52jdk2Xa86FGB')  
#auth2.set_access_token('915367269580107776-QscwJ8ZnJMa4LRQosrXuyj6xRg9PQs5','oKOZ488DFeSD1O1Jd6Nopburq6GvDUxCqqhvXptUFt9ko')  
#api2 = tweepy.API(auth2)

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
        print 'Connecting to new mongo collection with name: ', mongoCollectionName
        self.mongo_collection = self.mongo_db[mongoCollectionName]

    def setPlaceName(self, placeName):
        self.placeName = placeName

    def setNumTweets(self, numTweets):
        self.numTweets = numTweets

    def isTweetUsable(self, place, userLanguage, isRetweet, body, urls):
        return place is not None \
               and place.name == self.placeName \
               and 'en' in userLanguage \
               and isRetweet is False \
               and body is not None \
            # and len(urls) == 0

    def printTweetDetails(self, body, place):
        print ''
        print 'Saving tweet from: ', place.name
        print body

    def on_status(self, status):

        body = self.status_wrapper.fill(status.text)
        isRetweet = status.retweeted
        userLanguage = status.user.lang
        urls = status.entities['urls']
        count = 0
        place = status.place
        followerCount = status.user.followers_count
        screenName = status.author.screen_name
        friendCount = status.user.friends_count
        createdAt = status.created_at
        messageId = status.id

        if self.isTweetUsable(place, userLanguage, isRetweet, body, urls):

            self.printTweetDetails(body, place)
            try:
                self.mongo_collection.insert({
                    'body': body,
                    'followers': followerCount,
                    'screen_name': screenName,
                    'friends_count': friendCount,
                    'created_at': createdAt,
                    'message_id': messageId,
                    'location': place.name,
                    'local_datetime': datetime.datetime.now()
                })
                count = self.mongo_collection.count()
                print 'tweets saved: %s', count
            except Exception, (e):
                print('Exception reached: ' + str(e))
                pass
            if count >= self.numTweets:
                raise TweetLimitReachedException("Ending stream")


def saveTweets(numTweets, mongoCollectionName, locationCoordinates, locationName):
    try:
        l = StreamListener()
        l.setPlaceName(locationName)
        l.setNumTweets(numTweets)
        l.setMongoCollection(mongoCollectionName)
#        if locationName in ['denver','boston','houston']:
#            authTok = auth2
#        else:
#            authTok = auth1
        streamer = tweepy.Stream(auth=auth1, listener=l, timeout=3000)

        streamer.filter(locations=locationCoordinates)
    except TweetLimitReachedException, (e):
        print str(e)


def getPlaceID(placeName):
    places = api.geo_search(query=placeName, granularity="city")
    place_id = places[0].id
    return place_id

def getNYCTweets():
    place_id = '01a9a39529b27f36'
    tweets = api.search(q="place:%s" % place_id, count=100)
    print "We found %s tweets" % str(len(tweets))

class TweetLimitReachedException(Exception):
   """Use this to end the stream"""
   pass