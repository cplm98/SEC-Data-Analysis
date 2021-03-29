# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 11:10:58 2021

@author: Grind
"""

import string
import collections
from nltk.stem import PorterStemmer
import pandas as pd
import numpy as np

doc1 = open("./doc1.txt.", "r").read()
doc2 = open("./doc2.txt", "r").read()

def tokenize(document):
    stemmer = PorterStemmer()
    document = document.translate(str.maketrans('', '', string.punctuation)) #remove punctuation
    arr = document.lower().split() #all to lowercase, remove spaces
    arr = [stemmer.stem(word) for word in arr] #stem words
    return arr
    

def tf(tokens, relative=True):
    n = len(tokens)
    freq = collections.defaultdict(float)
    
    for token in tokens:
        freq[token] = freq[token] + 1/n if relative else freq[token] + 1
        
    return freq

def tfidf(corpus):
    n_doc = len(corpus)
    combined = []
    tfreq_array = []
    
    for document in corpus:
        tokens = tokenize(document)
        combined += tokens
        tfreq_array.append(tf(tokenize(document)))
    
    data = pd.concat( [pd.DataFrame(tfreq_array[i], index=[0]).T for i in range(len(tfreq_array))] , keys=list(range(len(tfreq_array))) )
    data.columns = ["tf"]
    
    data["df"] = data.index.get_level_values(1).map( data.index.get_level_values(1).value_counts() )
    
    data["tfidf"] = np.log( n_doc*1/data["df"] )

    return data


out = (tfidf([doc1,doc2]))
    
        