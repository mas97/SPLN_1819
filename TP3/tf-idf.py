#w i,j = tf i,j * log (N/df i)
#tf i,j -> número de ocorrencias de i no documento j
#N -> número de documentos
#df i -> número de documentos que contêm i

import pickle
import math
import pandas as pd
from operator import itemgetter

def load_obj(name):
    with open(name + '.pkl', 'rb') as fp:
        return pickle.load(fp)

dict = load_obj("dict_movies_list_words")
dict2 = {k: dict[k] for k in list(dict)[:500]}

testDict = {'docA' :"The cat sat on my", 'docB' :"The dog sat on my bed"}

def buildWordCountDict(dict_movies):
    dict = {}
    for movie,words in dict_movies.items():
        dict[movie] = {}
        for word in words.split():
            if word in dict[movie]:
                dict[movie][word] = dict[movie][word] + 1
            else:
                dict[movie][word] = 1
    return dict

def computeTF(wordDict):
    tfDict = {}
    for movie,words in wordDict.items():
        tfDict[movie] = {}
        totalMovieWords= len(wordDict[movie])
        for word,freq in words.items():
            tfDict[movie][word] = freq / totalMovieWords
    return tfDict

def computeIDF(wordDict):
    idfDict = {}
    totalMovies= len(wordDict)
    wordOnDocuments = {}

    for movie, words in wordDict.items():
        for word in words:
            if word in wordOnDocuments:
                wordOnDocuments[word] = wordOnDocuments[word] + 1
            else:
                wordOnDocuments[word] = 1
    for movie,words in wordDict.items():
        idfDict[movie] = {}
        for word in words:
            idfDict[movie][word] = math.log10(totalMovies / wordOnDocuments[word])
    return idfDict

def computeTFIDF(wordDict, tfDict, idfDict):
    tfidfDict = {}
    for movie, words in wordDict.items():
        tfidfDict[movie]= {}
        for word in words:
            tfidfDict[movie][word] = tfDict[movie][word] * idfDict[movie][word]
    return tfidfDict


def buildTFIDF(dict_movies):
    wordDict = buildWordCountDict(dict_movies)
    tfDict = computeTF(wordDict)
    idfDict = computeIDF(wordDict)
    tfidfDict = computeTFIDF(wordDict, tfDict, idfDict)
    return tfidfDict

def orderDict(tfidfDict):
    orderDict = {}
    for movie,words in tfidfDict.items():
        orderDict[movie] = []
        orderDict[movie] = sorted(words.items(), key=itemgetter(1),reverse=True)
    return orderDict

def match(orderDict,movieRequest):
    if movieRequest in orderDict:
        mostImportantWords= orderDict[movieRequest][:10]
        print("RequestMovie-->")
        print(mostImportantWords)
        suggestiveFilms= []
        for movie, words in orderDict.items():
            if movieRequest != movie :
                aux = words[:10]
                print(movie + '-->')
                print(aux)
                if aux == mostImportantWords:
                    suggestiveFilms.append(movie)
        print("--SUGGEST--")
        print(suggestiveFilms)
    else :
        print('No film on dataset, try another')
    

tfidfDict = buildTFIDF(dict2) #Dict = {"movie1": {"palavra1": tfidf value, "palavra2": tfidf value}, "movie2": {"palavra1": tfidf value}}
orderDict = orderDict(tfidfDict) #Dict = {"movie1:" [('palavra1',tfidf value), ('palavra2', tfidf value)], "movie2": ['palavra1':tfidf value]}
suggestiveFilms = match(orderDict, 'Batman')
#print(orderDict.keys())
#print(pd.DataFrame(tfidfDict))




