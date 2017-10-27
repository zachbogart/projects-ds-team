#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 13:33:47 2017

@author: michelkauffmann
"""

def sentiment_dict(sentimentData):
    afinnfile = open(sentimentData)
    scores = {} 
    for line in afinnfile:
        term, score = line.split("\t") 
        scores[term] = float(score) 

    return scores 

def enrichWithSentiment(inputFileName, outputFileName):
    import json
    with open(inputFileName) as data_file:    
        data = json.load(data_file)
        for tweet in data:
            tweet_body = (tweet['body'])
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
            tweet['sentScore'] = sent_score
            with open(outputFileName, 'w') as outfile:  
                json.dump(data, outfile)
    return

sentimentData = 'wordwithStrength.txt'
sentScores = sentiment_dict(sentimentData)
