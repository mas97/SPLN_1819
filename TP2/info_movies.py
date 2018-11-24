#! /usr/bin/env python3
import requests
from imdb import IMDb
from bs4 import BeautifulSoup

def info_movie(url):
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    print('Título: ' + soup.find('h1').contents[0])
    info = soup.find('div', class_='subtext')
    print('Restrição de idade: ' + info.contents[0].strip())
    print('Duração: ' + info.time.string.strip())
    print('Géneros: ' + ', '.join([g.string for g in info.findAll('a')[:-1]]))
    print('Data de estreia: ' + info.findAll('a')[-1].string)

movie = input('Nome do filme: ')
ia = IMDb()
results = ia.search_movie(movie)
mv = results[0] #First result
URL = ia.get_imdbURL(mv) #URL for first result
info_movie(URL)
