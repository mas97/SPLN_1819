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

def orderTFIDFvalues(tfidfDict):
    orderDict = {}
    for movie,words in tfidfDict.items():
        orderDict[movie] = []
        orderDict[movie] = sorted(words.items(), key=itemgetter(1),reverse=True)
    return orderDict

def match_count(mostImportantWords,aux):
    mostImportantWordsFirstTuple= [t[0] for t in mostImportantWords]
    auxFirstTuple = [t[0] for t in aux]
    equalElem = set(mostImportantWordsFirstTuple) & set(auxFirstTuple)
    return len(equalElem)

def match(movieRequest):
    tfidfDict = buildTFIDF(dict) #Dict = {"movie1": {"palavra1": tfidf value, "palavra2": tfidf value}, "movie2": {"palavra1": tfidf value}}
    orderDict = orderTFIDFvalues(tfidfDict) #Dict = {"movie1:" [('palavra1',tfidf value), ('palavra2', tfidf value)], "movie2": ['palavra1':tfidf value]}
    suggestFilms = []
    if movieRequest in orderDict:
        mostImportantWords= orderDict[movieRequest][:10]
        print("RequestMovie-->")
        print(mostImportantWords)
        for movie, words in orderDict.items():
            if movieRequest != movie :
                aux = words[:10]
                #print(movie + '-->')
                #print(aux)
                suggestFilms.append((movie,match_count(mostImportantWords,aux)))
        suggestFilms = sorted(suggestFilms, key=lambda tup: tup[1], reverse = True)
        print("--SUGGEST--")
        print(suggestFilms[:10])
    else :
        print('No film on dataset, try another')
    

suggestiveFilms = match('Batman')
#print(pd.DataFrame(tfidfDict))




