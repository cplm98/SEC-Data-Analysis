# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 15:13:25 2021

@author: Grind
"""

#from CNN_improved import ConvNet
import os
from tf_idf import tfidf

def loadCorpus(folder):
    corpus = []
    fileList = []
    for subdir, dirs, files in os.walk(folder):
        for file in files:
            path = os.path.join(subdir, file)
            if path[-3:] == 'txt':
                ticker = path[len(folder) + 1:]
                ticker = ticker[:ticker.index('/')]
                year = path[path.index('_') + 1:path.index('_') + 5]
                fileList.append(ticker+'-'+year)
                report = open(path,'r').read()
                corpus.append(report)
    return corpus, fileList


corpus, fileList = loadCorpus('data-part1')
data = tfidf(corpus)

data.to_csv('tfidf.csv')

with open("documentNames.txt", "w") as f:
    for fileName in fileList:
        f.write(str(fileName) +"\n")





