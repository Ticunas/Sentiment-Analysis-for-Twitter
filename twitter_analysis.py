#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 02:12:26 2018

@author: Tadman Reis

"""

import tweepy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from credentials import *
from sentiment_analysis import *
import copy

"""
Please check credentials.py before use.
You need add your Twitter Api key first
""" 
def twitter_setup():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    
    api = tweepy.API(auth)
    return api

#Create extractor
def extrect_by_name(name):
    extrector = twitter_setup()
    tweets = extrector.user_timeline(screen_name=name, count=200)
    print("number of tweets extracted: {}.\n".format(len(tweets)))    
    #Creating dataframe    
    global data
    data = pd.DataFrame(data=[tweet.created_at for tweet in tweets], columns=['Date'])
    data['Tweets'] = np.array([tweet.text for tweet in tweets])
    data['len']  = np.array([len(tweet.text) for tweet in tweets])
    data['ID']   = np.array([tweet.id for tweet in tweets])
    data['Source'] = np.array([tweet.source for tweet in tweets])
    data['Likes']  = np.array([tweet.favorite_count for tweet in tweets])
    data['RTs']    = np.array([tweet.retweet_count for tweet in tweets])
    #data['SA'] = np.array([analize_sentiment(tweet) for tweet in data['Tweets']])
    data['SA'] = np.array([analyse_setence(tweet) for tweet in data['Tweets']])
        
    return data


def mean_tweets_lenghts():
    mean = np.mean(data['len'])
    print("The lenght's avarage in tweets: {}".format(mean))
    return

def max_likes():
    max_likes = np.max(data['Likes'])
    index_most_liked = data[data.Likes == max_likes].index[0]
    print("The tweet with more likes is: \n{}".format(data['Tweets'][index_most_liked]))
    print("Number of likes: {}".format(max_likes))
    return


def mean_sentiment_analysis():
    positive_tweets = [ tweet for index, tweet in enumerate(data['Tweets']) if data['SA'][index] > 0 ]
    neutral_tweets  = [ tweet for index, tweet in enumerate(data['Tweets']) if data['SA'][index] == 0]
    negative_tweets = [ tweet for index, tweet in enumerate(data['Tweets']) if data['SA'][index] < 0 ]
    
    print("Percentage of positive tweets: {}%".format(len(positive_tweets)*100/len(data['Tweets'])))
    print("Percentage of neutral tweets: {}%".format(len(neutral_tweets)*100/len(data['Tweets'])))
    print("Percentage de negative tweets: {}%".format(len(negative_tweets)*100/len(data['Tweets'])))
    
    return

#sentiment analysis is showed as1 for the most positive and -1 for most negative
def plot_sentiment_analysis():
    plt.plot(np.array(data['Date']), np.array(data['SA']), color='blue')
    plt.title('Sentiment Analysis')
    plt.ylabel('Sentiment')
    plt.xticks(rotation=90)
    plt.show()
    return

def most_negative():
    most_neg = np.min(data['SA'])
    index_most_neg = data[data.SA == most_neg].index[0]
    print("Polarity: {}".format(most_neg))
    print("Most Negative Tweet: \n{}\n\n".format(data['Tweets'][index_most_neg]))
    return

def most_positive():
    most_pos = np.max(data['SA'])
    index_most_pos = data[data.SA == most_pos].index[0]
    print("Polarity: {}".format(most_pos))
    print("Most Positive Tweet: \n{}".format(data['Tweets'][index_most_pos]))
    return

def extrect_by_hashtag(hashtag):
    extrector = twitter_setup()
    cursor = tweepy.Cursor(extrector.search, q=hashtag, rpp=100).items(20)
    tweets = list(cursor)
    
    global data
    data = pd.DataFrame(data=[tweet.created_at for tweet in tweets], columns=['Date'])
    data['Author'] = np.array([tweet.user.screen_name for tweet in tweets])
    data['Tweets'] = np.array([tweet.text for tweet in tweets])
    data['len']  = np.array([len(tweet.text) for tweet in tweets])
    data['ID']   = np.array([tweet.id for tweet in tweets])
    data['Source'] = np.array([tweet.source for tweet in tweets])
    data['Likes']  = np.array([tweet.favorite_count for tweet in tweets])
    data['RTs']    = np.array([tweet.retweet_count for tweet in tweets])
    #data['SA'] = np.array([analize_sentiment(tweet) for tweet in data['Tweets']])
    data['SA'] = np.array([analyse_setence(tweet) for tweet in data['Tweets']])
    return
    
if __name__ == "__main__":
    
    #Menu
    option = -1
    while  option!='0':
        print("1 - Analyze by name")
        print("2 - Analyze by Hashtag")
        print("0 - exit")
        print("Select a Option:")
        
        option = input()
        
        if(option=='1'):
            print("Insert twitter name to analyse")
            name = input()
            extrect_by_name(name)
            mean_sentiment_analysis()
            print()
            plot_sentiment_analysis()
            print()
            most_negative()
            print()
            most_positive()
            
        elif(option=='2'):
            print("Insert twitter hashtag (withou '#') to analyse")
            hashtag = input()
            extrect_by_hashtag(hashtag)
            mean_sentiment_analysis()
            print()
            plot_sentiment_analysis()
            print()
            most_negative()
            print()
            most_positive()
            
    
    
    

