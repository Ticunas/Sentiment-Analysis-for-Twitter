#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 00:38:05 2018

@author: Tadman Reis
"""
from nltk.classify import NaiveBayesClassifier
import pandas as pd
import re

def _word_feats(words):
    return dict([(word, True) for word in words])


def _clean_sentence(sentence):
    sentence = sentence.lower()
    sentence =  ' '.join(re.sub("(@[a-zA-Zà-úÀ0-Ú0-9]+)|([^a-zA-Zà-úÀ0-Ú0-9]| (\w+:\/\/\S+))", 
                                " ", sentence).split())
    return sentence.split(' ')



def analyse_setence(sentence):
    _creating_classifier()
    words = _clean_sentence(sentence)
    
    neg = 0
    pos = 0
    
    for word in words:
        classResult = classifier.classify( _word_feats(word))
        if classResult == 'neg':
            neg = neg + 1
        if classResult == 'pos':
            pos = pos + 1
            
    result = (float(pos)/len(words) - (float(neg)/len(words)))
    return result

def _creating_classifier():
    """
    You can use your own dictionary
    """
    dataframe = pd.read_csv('Dictionary_pt - Sheet1.csv')
    positive_words = dataframe['Positive']
    negative_words = dataframe['Negative']
    neutral_words = dataframe['Neutral']
    
    positive_features = [(_word_feats(pos), 'pos') for pos in positive_words]
    negative_features = [(_word_feats(neg), 'neg') for neg in negative_words]
    neutral_features = [(_word_feats(neu), 'neu') for neu in neutral_words]
    
    
    train_set = negative_features + positive_features + neutral_features
    global classifier 
    classifier = NaiveBayesClassifier.train(train_set) 
    

        
