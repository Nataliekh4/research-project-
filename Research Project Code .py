# -*- coding: utf-8 -*-
"""
Created on Sun May 10 16:52:19 2020

@author: Admin
"""

from nltk.tokenize import SyllableTokenizer
from nltk import word_tokenize
import json
import os
import panphon
import numpy as np





def openBook():
    return open(r'C:\Users\Admin\Downloads\Word_timing 1\florin_500days_words_and_time_dtw.json')


def syllables(word):
    SSP = SyllableTokenizer()
    return SSP.tokenize(word)

def acousticArrayValues(syllable):
    properties = ['son', 'cons', 'cont', 'delrel', 'lat', 'nas', 'strid', 'voi', 'sg', 'cg', 'ant', 'cor', 'distr', 'lab', 'hi', 'lo', 'back', 'round', 'velaric', 'tense', 'long']
    ft=panphon.FeatureTable()
    acoustic_array = ft.word_array(properties, syllable)
    return np.sum(acoustic_array, axis=0)

def acousticArraySum(syllables):
    return list(map(lambda syllable : acousticArrayValues(syllable), syllables))

def acousticArrayForWord(syllables): 
    return np.sum(acousticArraySum(syllables), axis=0)

def main():
    book = openBook()
    summerdays = json.load(book)
    summerdays_words = list(map(lambda occurrence : occurrence[0], summerdays))
    summerdays_time = list(map(lambda occurrence : occurrence[1], summerdays))

    
    summerdays_syllables = list(map(syllables, summerdays_words))
    summedSummerdays = list(map(lambda syllables : acousticArrayForWord(syllables) ,summerdays_syllables))
    
    
    summerdays_time_start= summerdays_time[::2]
    summerdays_time_duration= summerdays_time[1::2]

   
    g = open(r"C:\Users\Admin\Desktop\summerdays_syllables.txt",'w')
    print(summerdays_syllables,file=g)

    f = open(r"C:\Users\Admin\Desktop\movie_words1.txt",'w')
    print(summerdays_words,file=f)
    
    n = open(r"C:\Users\Admin\Desktop\movie_times1.txt",'w')
    print(summerdays_time,file=n)
    
    #does the first 10 words 
    #x = 10
    print(list(zip(summerdays_words, summedSummerdays, summerdays_time_start, summerdays_time_duration)))
    
    #saves file 
    np.savetxt('results.csv', [p for p in zip(summerdays_words, summedSummerdays, summerdays_time_start, summerdays_time_duration)], delimiter=',', fmt='%s')

    

    
if __name__ == "__main__":
    main()
    
