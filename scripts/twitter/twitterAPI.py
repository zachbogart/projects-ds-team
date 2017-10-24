# -*- coding: utf-8 -*-

import tweepy
from pymongo import MongoClient
from textwrap import TextWrapper
from tweepy.utils import import_simplejson
json = import_simplejson()

auth1 = tweepy.auth.OAuthHandler('eOihmPsLf6q0ro03OFyDExyaH', 'XfOAN3SYME0vCRaaUqCsbbxUxNR88JdRKjLswqyGuZZ7fdfeB3')
auth1.set_access_token('2847047537-wwYPjhsb78FltOxFk8nFvvCtWD6zCVs9JE9qghh',
                       '4fjuf9awSDlNT3AsU7FZFu9AzQcIysKfX0b5IOetxkBr7')
api = tweepy.API(auth1)


# searchResults = api.search(searchQuery)
# for searchResult in searchResults:
#    actualResult = searchResult.text
#    parsed = json.loads((searchResult.text))
#    print json.dumps(parsed, indent=4, sort_keys=True)

class StreamListener(tweepy.StreamListener):
    mongo = MongoClient('localhost', 27017)
    mongo_db = mongo['twitterData']
    mongo_collection = mongo_db['Default']

    count = 0
    status_wrapper = TextWrapper(width=140, initial_indent='', subsequent_indent='')
    numTweets = 2

    def setMongoCollection(self, mongoCollectionName):
        self.mongo_collection = self.mongo_db[mongoCollectionName]

    def on_status(self, status):
        tempA = self.status_wrapper.fill(status.text)
        tempB = status.retweeted
        tempC = status.user.lang
        tempD = status.geo
        if ((('en' in tempC) and (tempB is False)) and (not ('RT') in tempA[:2]) and (
            ((('http' or 'www') in tempA) and ((' ') in tempA)) or (
        not ('http' or 'www') in tempA)) and tempA is not None):
            try:
                body = self.status_wrapper.fill(status.text)
                print ''
                print ''
                print body
                print ''
                self.mongo_collection.insert({
                    'body': body,
                    'followers': status.user.followers_count,
                    'screen_name': status.author.screen_name,
                    'friends_count': status.user.friends_count,
                    'created_at': status.created_at,
                    'message_id': status.id,
                    'location': status.user.location
                })
                count = self.mongo_collection.count()
                print 'tweets saved: %s', count
            except Exception, (e):
                print('Exception reached: ' + str(e))
                pass
            if count >= self.numTweets:
                raise Exception("Ending stream")


def saveTweets(numTweets, searchTerms, mongoCollectionName):
    try:
        l = StreamListener()
        l.numTweets = numTweets
        l.setMongoCollection(mongoCollectionName)
        streamer = tweepy.Stream(auth=auth1, listener=l, timeout=3000)
        streamer.filter(None, searchTerms)
    except Exception, (e):
        print str(e)
