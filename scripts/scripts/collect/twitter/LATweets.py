#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 21:46:51 2017

@author: michelkauffmann
"""
import os
import tweepy
from pymongo import MongoClient
from textwrap import TextWrapper
from tweepy.utils import import_simplejson
json = import_simplejson()

auth1 = tweepy.auth.OAuthHandler('5b4MTdzfuBx6ZIzzuYd6ydO1t',
                                 '	IorreG6GPrIHU96IewjyTnwD5UADd7mjIo3OUsCw3CbpxlsVeO')
auth1.set_access_token('920172026-Os69J1zjuuvucyYJ1LFtYby1S0lT0n6qaGi0nQtd',
                       '6ZuVQ4ersgQKHJpQT0fDTsBalZTcA2AzFJKgsP01GLd10')
api = tweepy.API(auth1)

os.chdir('/Users/michelkauffmann/desktop/Columbia Files/Projects in Data Science/Homework/Project/')

class StreamListener(tweepy.StreamListener):
    mongo = MongoClient('localhost', 27017)
    mongo_db = mongo['LATweets']
    mongo_collection = mongo_db['Default']

    status_wrapper = TextWrapper(width=140, initial_indent='', subsequent_indent='')

    def setMongoCollection(self, mongoCollectionName):
        self.mongo_collection = self.mongo_db[mongoCollectionName]

    def on_status(self, status):
        tempA = self.status_wrapper.fill(status.text)
        tempB = status.retweeted
        tempC = status.user.lang
        tempD = status.geo
        if ((('en' in tempC) and (tempB is False)) and (not ('RT') in 
             tempA[:2]) and (((('http' or 'www') in tempA) and ((' ') in 
                  tempA)) or (not ('http' or 'www') in tempA)) and tempA is not None):
            try:
                body = self.status_wrapper.fill(status.text)
                print ''
                print ''
                print body
                print ''
                sentScore = getSentScore(body)
                tweetWeather = getWeather(status.created_at)
                self.mongo_collection.insert({
                    'body': body,
                    'followers': status.user.followers_count,
                    'screen_name': status.author.screen_name,
                    'friends_count': status.user.friends_count,
                    'created_at': status.created_at,
                    'message_id': status.id,
                    'location': status.user.location,
                    'sentscore': sentScore,
                    'airtemp': tweetWeather.loc[:,'airtemp(C)'],
                    'dewpoint': tweetWeather.loc[:,'dewpoint(C)'],
                    'windspeed': tweetWeather.loc[:,'windspeed(m/s)'],
                    'skycoverage': tweetWeather.loc[:,'skycoverage(code)'],
                    '1h-prec': tweetWeather.loc[:,'1h-prec(mm)']
                })
                count = self.mongo_collection.count()
                print 'tweets saved: %s', count
            except Exception, (e):
                print('Exception reached: ' + str(e))
                pass
           
                
def getPlaceID():
    places = api.geo_search(query="Los Angeles", granularity="city")
    place_id = places[0].id
    print places
    print place_id
    print places[0].bounding_box.coordinates

##################### Get sentiment score for each tweet ######################

def sentiment_dict(sentimentData):
    afinnfile = open(sentimentData)
    scores = {} 
    for line in afinnfile:
        term, score = line.split("\t") 
        scores[term] = float(score) 

    return scores 

sentimentData = 'wordwithStrength.txt'
sentScores = sentiment_dict(sentimentData)

def getSentScore(tweet_body):
    try:
        if tweet_body:
            tweet_word = tweet_body.lower().split()
            # print tweet_word
            sent_score = 0
            for word in tweet_word:
                word = word.rstrip('?:!.,;"!@')
                word = word.replace("\n", "")
                if word in sentScores.keys():
                    # print word
                    sent_score = sent_score + float(sentScores[word])
                else:
                    sent_score = sent_score  
    except Exception, (e):
        print str(e)
    
    return sent_score

########################## Get weather for each tweet #########################
import pytz
from datetime import datetime
from email.utils import parsedate_tz, mktime_tz
    
def getWeather(created_at):
    timestamp = mktime_tz(parsedate_tz(created_at))
    dt = datetime.fromtimestamp(timestamp, pytz.timezone('US/Pacific'))
    tweet_month = dt.month
    tweet_day = dt.day
    tweet_hour = dt.hour

    weather_data = weather[(weather.month == tweet_month) & (weather.day == 
                           tweet_day) & (weather.hour == tweet_hour)]

    return weather_data 


def fetch_weather_data(url):
    import urllib2
    import StringIO
    import gzip
    import pandas as pd

    parse = [(0, 4),(4,7),(7,10),(10,13),(13,20),(20,25),(38,43),(44,49),
             (50,55),(56,61)]

    response = urllib2.urlopen(url)
    compressedFile = StringIO.StringIO()
    compressedFile.write(response.read())

    compressedFile.seek(0)
    decompressedFile = gzip.GzipFile(fileobj=compressedFile, mode='rb')
    weather_hist = pd.read_fwf(filepath_or_buffer=decompressedFile, 
                               colspecs=parse, header=None)
    
    return weather_hist


def parse_data(start_year, end_year, stationID):
    import pandas as pd
    baseURL = "ftp://ftp.ncdc.noaa.gov/pub/data/noaa/isd-lite/"

    col_names = ['year', 'month', 'day', 'hour', 'airtemp(C)', 'dewpoint(C)', 
                 'windspeed(m/s)', 'skycoverage(code)', '1h-prec(mm)', '6h-prec(mm)']
    full_hist = pd.DataFrame()
    
    for year in range(start_year,end_year+1):

        try:
            year_hist = fetch_weather_data(baseURL + str(year) + "/" + 
                                           str(stationID) + "-" + str(year) + ".gz")
            full_hist = full_hist.append(year_hist)
        except:
            print "following URL was invalid: " + baseURL + str(year) + "/" + str(stationID) + "-" + str(year) + ".gz"
            print "make sure to enclose the stationID in quotes"

    full_hist.columns = col_names
    
    return full_hist
    # full_hist.to_csv(str(stationID)+"_"+str(start_year)+"-"+str(end_year)+"_data.csv")
    

# Generate Weather DF
weather = parse_data(2017, 2017, '722950-23174')

l = StreamListener()
streamer = tweepy.Stream(auth=auth1, listener=l, timeout=3000)
streamer.filter(locations=[-118.668404,33.704538,-118.155409,34.337041])



