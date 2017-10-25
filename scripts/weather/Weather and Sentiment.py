#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 13:05:09 2017

@author: michelkauffmann
"""

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

    weather_data = weather[(weather.month == tweet_month) & (weather.day == tweet_day) & (weather.hour == tweet_hour)]

    return weather_data 


def fetch_weather_data(url):
    import urllib2
    import StringIO
    import gzip
    import pandas as pd

    parse = [(0, 4),(4,7),(7,10),(10,13),(13,20),(20,25),(38,43),(44,49),(50,55),(56,61)]

    response = urllib2.urlopen(url)
    compressedFile = StringIO.StringIO()
    compressedFile.write(response.read())

    compressedFile.seek(0)
    decompressedFile = gzip.GzipFile(fileobj=compressedFile, mode='rb')
    weather_hist = pd.read_fwf(filepath_or_buffer=decompressedFile, colspecs=parse, header=None)
    
    return weather_hist


def parse_data(start_year, end_year, stationID):
    import pandas as pd
    baseURL = "ftp://ftp.ncdc.noaa.gov/pub/data/noaa/isd-lite/"

    col_names = ['year', 'month', 'day', 'hour', 'airtemp(C)', 'dewpoint(C)', 'windspeed(m/s)', 'skycoverage(code)', '1h-prec(mm)', '6h-prec(mm)']
    full_hist = pd.DataFrame()
    
    for year in range(start_year,end_year+1):

        try:
            year_hist = fetch_weather_data(baseURL + str(year) + "/" + str(stationID) + "-" + str(year) + ".gz")
            full_hist = full_hist.append(year_hist)
        except:
            print "following URL was invalid: " + baseURL + str(year) + "/" + str(stationID) + "-" + str(year) + ".gz"
            print "make sure to enclose the stationID in quotes"

    full_hist.columns = col_names
    
    return full_hist
    #full_hist.to_csv(str(stationID)+"_"+str(start_year)+"-"+str(end_year)+"_data.csv")


weather = parse_data(2017, 2017, '722950-23174')
getSentScore("This is a great time to be alive")
tweet_weather = getWeather("Wed Aug 27 13:08:45 +0000 2008")
