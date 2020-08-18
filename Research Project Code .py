# -*- coding: utf-8 -*-
"""
Created on Sun May 10 16:52:19 2020

@author: Admin
"""

import json
import os
import panphon
import numpy as np
from collections import Counter 
import eng_to_ipa as ipa



def openBook():
    return open(r'C:\Users\Admin\Desktop\Research Project\12_years_a_slave.json')

def ipaConvert(word):
    return ipa.convert(word)

def acousticArrayValues(word):
    properties = ['syl', 'son', 'cons', 'cont', 'delrel', 'lat', 'nas', 'strid', 'voi', 'sg', 'cg', 'ant', 'cor', 'distr', 'lab', 'hi', 'lo', 'back', 'round', 'velaric', 'tense', 'long']
    ft=panphon.FeatureTable()
    acoustic_array = ft.word_array(properties, word)
    return np.sum(acoustic_array > 0, axis=0)

def acousticArrayValuesNeg(word):
    properties = ['syl', 'son', 'cons', 'cont', 'delrel', 'lat', 'nas', 'strid', 'voi', 'sg', 'cg', 'ant', 'cor', 'distr', 'lab', 'hi', 'lo', 'back', 'round', 'velaric', 'tense', 'long']
    ft=panphon.FeatureTable()
    acoustic_array = ft.word_array(properties, word)
    return ((acoustic_array<0)*acoustic_array).sum(axis=0) 

def phonemeCount(word):
    properties = ['syl', 'son', 'cons', 'cont', 'delrel', 'lat', 'nas', 'strid', 'voi', 'sg', 'cg', 'ant', 'cor', 'distr', 'lab', 'hi', 'lo', 'back', 'round', 'velaric', 'tense', 'long']
    ft=panphon.FeatureTable()
    acoustic_array = ft.word_array(properties, word)
    return (acoustic_array.shape[0])

def generateRow(occurrence):
    word = occurrence['subtitle']
    start_time = occurrence['start_time_new']
    end_time = occurrence['end_time_new']
    interval = occurrence['interval_new'] 
    summedAcousticArray = acousticArrayValues(ipaConvert(word)).tolist()
    summedAcousticArrayNeg = acousticArrayValuesNeg(ipaConvert(word)).tolist()
    positive_values_count = len(list(filter(lambda x : x > 0, summedAcousticArray)))
    num_0s = summedAcousticArray.count(0)
    phonemecounts = phonemeCount(ipaConvert(word))


    
    list_of_values = summedAcousticArrayNeg + summedAcousticArray + [positive_values_count] + [phonemecounts] + [num_0s]
    return str(start_time) + "*" + ','.join([str(i) for i in list_of_values]) + ":" + str(interval)
    

def main():
    book = openBook()
    summerdays = json.load(book)
    
    summerdays_rows = list(map(lambda occurrence : generateRow(occurrence), summerdays))
    
 
    

     
    np.savetxt('12_years_a_slave', summerdays_rows, fmt='%s')
   

   

    
if __name__ == "__main__":
    main()
    

    
