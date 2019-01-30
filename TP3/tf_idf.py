#w i,j = tf i,j * log (N/df i)
#tf i,j -> número de ocorrencias de i no documento j
#N -> número de documentos
#df i -> número de documentos que contêm i

import pickle
import math
import pandas as pd
from operator import itemgetter
from scraping import save_obj,load_obj,get_movies_url,save_full_scripts

#testDict = {'docA' :"The cat sat on my", 'docB' :"The dog sat on my bed"}
nFilms = 10
topWords = 50
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

def match_count(mostImportantWords,movieWords):
    mostImportantWordsFirstTuple= [t[0] for t in mostImportantWords]
    movieWordsFirstTuple = [t[0] for t in movieWords]
    equalElem = set(mostImportantWordsFirstTuple) & set(movieWordsFirstTuple)
    return len(equalElem)

def match_genre_count(suggestFilms,lower_value,movieRequest):
    match = []
    for t in suggestFilms[nFilms:]:
        if t[1]!=lower_value:
            break
        else:
            match.append((t[0],len(set(genresDict[movieRequest]) & set(genresDict[t[0]]))))
    match = sorted(match, key=lambda tup: tup[1], reverse = True)
    #for m in match[:10]:
    #    print(m[0])
    #    print(genresDict[m[0]])
    return match

def genres_ok(suggestFilms, movieRequest):
    #print('--sugest filme--')
    #print(genresDict[movieRequest])
    lower_value = suggestFilms[nFilms][1]
    match_genre = match_genre_count(suggestFilms,lower_value,movieRequest)
    for n,t in enumerate(suggestFilms[:nFilms]):
        if t[1]==lower_value:
            if len(match_genre)>0 and match_genre[0][1]>0 and len(set(genresDict[t[0]]) & set(genresDict[movieRequest])) < match_genre[0][1]:
                suggestFilms[n]=match_genre[0]
                del match_genre[0]
    return suggestFilms


def match(movieRequest):
    #print(movieRequest)
    suggestFilms = []
    if movieRequest in orderDict:
        mostImportantWords= orderDict[movieRequest][:topWords]
        for movie, words in orderDict.items():
            if movieRequest != movie :
                movieWords = words[:topWords]
                suggestFilms.append((movie,match_count(mostImportantWords,movieWords)))
        suggestFilms = sorted(suggestFilms, key=lambda tup: tup[1], reverse = True)
        #print("--SUGGESTÕES ANTES DE TRATAR GENERO--")
        #print(suggestFilms[:nFilms])
        suggestFilms = genres_ok(suggestFilms,movieRequest)
        #print("--SUGGESTÕES FINAIS--")
        #print(suggestFilms[:nFilms])
        suggestFilmsGenres = []
        for movie in suggestFilms[:nFilms]:
            suggestFilmsGenres.append((movie[0],genresDict[movie[0]]))
        #print("--RESULTADOS--")
        #print(suggestFilmsGenres)
        return suggestFilmsGenres
    else :
        #print("Não há esse filme no dataset")
        return []

try:  
    filmsDict = load_obj("dict_movies_list_words")
    genresDict = load_obj("dict_movies_list_genres")
except Exception:
    list_urls = get_movies_url()
    save_full_scripts(list_urls)
try:
    orderDict = load_obj("dict_tfidf_movies_order")
except Exception:
    tfidfDict = buildTFIDF(filmsDict) #Dict = {"movie1": {"palavra1": tfidf value, "palavra2": tfidf value}, "movie2": {"palavra1": tfidf value}}
    orderDict = orderTFIDFvalues(tfidfDict) #Dict = {"movie1:" [('palavra1',tfidf value), ('palavra2', tfidf value)], "movie2": ['palavra1':tfidf value]}    
    save_obj(orderDict,'dict_tfidf_movies_order')

#suggestFilms = match('12 and holding')

#print(pd.DataFrame(tfidfDict))
#print(len(filmsDict))
#print(len(orderDict))
#print(len(genresDict))

#for movie in orderDict:
#    if movie in genresDict:
#        pass
#    else:
#        print(movie)

#print(filmsDict['nightmare on elm street the final chapter'])
#print(genresDict['nightmare on elm street the final chapter'])





