import string, os, re
import numpy as np
import pandas as pd
from nltk.stem import PorterStemmer



# Tokenize function from tf-idf.py file for consistency
def tokenize(document):
    stemmer = PorterStemmer()
    document = document.translate(str.maketrans('', '', string.punctuation)) #remove punctuation
    arr = document.lower().split() #all to lowercase, remove spaces
    arr = [stemmer.stem(word) for word in arr] #stem words
    return arr


# Takes all documents in folder provided and adds words in 
# txt file to vocab which is then saved
def createVocab(folder):
    vocab = set()
    for subdir, dirs, files in os.walk(folder):
        for file in files:
            path = os.path.join(subdir, file)
            if path[-3:] == 'txt':
                report = open(path,'r').read()
                words = tokenize(report)
                for word in words:
                    vocab.add(word)
    with open("vocab.txt", "w") as output:
        output.write(str(vocab))

# Loads vocab txt file and returns words in a list
def loadVocab(path, vocabType = 'all'):
    vocab = open(path,'r').read()
    vocab = vocab.strip('{}').split(',')
    vocabList = []
    if vocabType == 'noNum':
        for word in vocab:
            if bool(re.search(r'\d', word)) == False:
                vocabList.append(word.strip(" '")) 
        return vocabList
    else:
        for word in vocab:
            vocabList.append(word.strip(" '")) 
        return vocabList

def makeBlankDict(vocab):
    blankDict = {}
    for word in vocab:
        blankDict[word] = 0
    return blankDict

def createVectors(vocab, folder):
    df = pd.DataFrame(columns=vocab)
    blankDict = makeBlankDict(vocab)
    for subdir, dirs, files in os.walk(folder):
        for file in files:
            path = os.path.join(subdir, file)
            if path[-3:] == 'txt':
                ticker = path[len(folder) + 1:]
                ticker = ticker[:ticker.index('/')]
                year = path[path.index('_') + 1:path.index('_') + 5]
                report = open(path,'r').read()
                words = tokenize(report)
                wordDict = getWordCounts(words, vocab)
                df.loc[ticker + '-' + year] = wordDict
    return df
                
        

# Returns a dictionary with word 
def getWordCounts(words, vocab):
    blankDict = makeBlankDict(vocab)
    for word in words:
        try:
            blankDict[word] += 1
        except:
            pass
    return blankDict




vocab = loadVocab('vocab.txt', 'noNum')
df = createVectors(vocab, 'data-part1')
df.to_csv('bow-df.csv')

