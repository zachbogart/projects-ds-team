# -*- coding: utf-8 -*-

import tweepy
from pymongo import MongoClient
from textwrap import TextWrapper

from requests.packages.urllib3.exceptions import ReadTimeoutError
import time

from tweepy.utils import import_simplejson
import datetime

json = import_simplejson()

auth1 = tweepy.auth.OAuthHandler('EeN161Gk3RqJAQd8zrimPckkF', '0wACEZgYxCoSzMuTa22LdZSfrTWo2BCfsnU6ggK7keeEcQXDqf')
auth1.set_access_token('2847047537-7vEFDI9rFnEb2h4HmiAJoxSglfurC57XNFTJamr',
                       '54CTHM5XeBYEsyogP6m2EijRUeLW0mTBaPxjMkiAMmyIf')
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
        print 'here 1'
        l.setPlaceName(locationName)
        print 'here 1'
        l.setNumTweets(numTweets)
        print 'here 1'
        l.setMongoCollection(mongoCollectionName)
        print 'here 1'
        streamer = tweepy.Stream(auth=auth1, listener=l, timeout=1)
        print 'here 1'
        # streamer.filter(locations=[-80,
        #     41,
        #     -80.1,
        #     41.1
        #                            ])
        print 'here 2'
        while True:
            try:
                streamer.filter(locations=locationCoordinates)
            except ReadTimeoutError, (e):
                print ''
                print e
                print 'we stopped'
                time.sleep(30)
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