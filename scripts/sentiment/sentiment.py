#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 13:33:47 2017

@author: michelkauffmann
"""
from scripts.utils import utils


def sentiment_dict(sentimentData):
    afinnfile = open(sentimentData)
    scores = {} 
    for line in afinnfile:
        term, score = line.split("\t") 
        scores[term] = float(score) 

    return scores 

def enrichWithSentiment(inputFilePath, outputFilePath):
    import json

    count = 0
    with open(inputFilePath) as data_file:
        data = json.load(data_file)
        print 'Adding sentiments to tweet list of length: ', len(data)
        for tweet in data:
            if count % 10000 == 0:
                print "Adding sentiment data: ", count
            count = count + 1
            tweet_body = (tweet['body'])
            try:
                if tweet_body:
                    tweet_word = tweet_body.lower().split()
                    # print tweet_word
                    sent_score = 0
                    for word in tweet_word:
                        word = word.rstrip('?:!.,;"!@')
                        word = word.replace("\n", "")
                        if word in sentScores:
                            # print word
                            sent_score = sent_score + float(sentScores[word])
            except Exception, (e):
                print str(e)
            tweet['sentiment'] = sent_score
        with open(outputFilePath, 'w') as outfile:
            json.dump(data, outfile)
    print 'File saved to ', outputFilePath
    return outputFilePath

sentimentDataPath = utils.getFullPathFromResourceFileName('wordwithStrength.txt')
sentScores = sentiment_dict(sentimentDataPath)
