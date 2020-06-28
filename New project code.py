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
import pandas as pd




def openBook():
    return open(r'C:\Users\Admin\Desktop\Research Project\500_days_of_summer.json')
  

def syllables(word):
    SSP = SyllableTokenizer()
    return SSP.tokenize(word)

def acousticArrayValues(word):
    properties = ['son', 'cons', 'cont', 'delrel', 'lat', 'nas', 'strid', 'voi', 'sg', 'cg', 'ant', 'cor', 'distr', 'lab', 'hi', 'lo', 'back', 'round', 'velaric', 'tense', 'long']
    ft=panphon.FeatureTable()
    acoustic_array = ft.word_array(properties, word)
    return np.sum(acoustic_array, axis=0)

def acousticArraySum(syllables):
    return list(map(lambda syllable : acousticArrayValues(syllable), syllables))

def acousticArrayForWord(syllables): 
    return np.sum(acousticArraySum(syllables), axis=0)

def generateRow(occurrence):
    word = occurrence['subtitle']
    start_time = occurrence['start_time_new']
    end_time = occurrence['end_time_new']
    interval= occurrence['interval_new'] 
    #syllablez = syllables(word)
    summedAcousticArray = acousticArrayValues(word)
    
    return [word, summedAcousticArray, start_time, end_time, interval]
    

def main():
    book = openBook()
    summerdays = json.load(book)

    
    summerdays_rows = list(map(lambda occurrence : generateRow(occurrence), summerdays[0:15])) 
    np.savetxt('results.csv', summerdays_rows, fmt='%s')
    
   
    
    
if __name__ == "__main__":
    main()
    
