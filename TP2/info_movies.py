#! /usr/bin/env python3

import sys
import getopt
import requests
import re
import nltk
from imdb import IMDb
from bs4 import BeautifulSoup

def info_movie(movie):
    ia = IMDb()
    results = ia.search_movie(movie)
    mv = results[0] #First result
    URL = ia.get_imdbURL(mv) #URL for first result
    page = requests.get(URL)
    page_text = page.text
    soup = BeautifulSoup(page_text, "html.parser")
    tag = soup.find('h1')
    print('Título: ' + tag.contents[0])
    info = soup.find('div', class_='subtext')
    age = info.contents[0]
    print('Restrição de idade: ' + age.strip())
    duration = info.time.string
    print('Duração: ' + duration.strip())
    genres = []
    i = 6
    while info.contents[i].name != 'span':
        tag = info.contents[i]
        genres.append(re.findall(r'\w+|$', tag.string)[0])
        i += 1
    print('Géneros: ' + ', '.join([g for g in genres if g]))
    print('Data de estreia: ' + info.contents[i+2].string)

movie = input('Nome do filme: ')
info_movie(movie)
