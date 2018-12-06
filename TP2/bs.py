#! /usr/bin/env python3

import sys
import getopt
import requests
import re
import string
import matplotlib.pyplot as plt
import numpy as np
import fileinput
from imdb import IMDb
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer

opts, args = getopt.getopt(sys.argv[1:], 'hbsac')
ops = dict(opts)

def build():
    """Coloca em ficheiro todos os filmes presentes no site: www.imsdb.com"""

    alphabet = "0ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    names_pages = []

    #reunião de todas as páginas de nomes de filmes
    for c in alphabet:
        print("Getting " + "https://www.imsdb.com/alphabetical/" + c)
        request = requests.get("https://www.imsdb.com/alphabetical/" + c)
        names_pages.append(request)
    for page in names_pages:
        page_soup = BeautifulSoup(page.text, "html.parser")
        results = page_soup.find_all('a')
        file = open("films_names", "a")
        for result in results:
            if re.search(r'<p>', str(result.parent)) and 'href' in result.attrs and 'title' in result.attrs:
                title = result.text.replace(' ', '-')
                title = title.replace(':', '')
                url = 'https://www.imsdb.com/scripts/' + title + '.html' + '\n'
                file.write(url)
        file.close()

def build_movies_db():
    movies_db = dict()
    for url in fileinput.input("films_names"):
        match = re.search(r'/(\w+(?:-\w+)*)\.html', url)
        if match:
            key = re.sub(r'-', r' ', match.group(1))
            key = key.lower()
            movies_db[key] = url.strip()
    return movies_db

def get_movie_url(movies_db):
    movie = input('Nome do filme: ')
    movie = movie.lower()
    search_result = []
    for m, url in movies_db.items():
        match = re.search(movie, m)
        if match:
            search_result.append(m)
    if len(search_result) > 1:
        for val, res in enumerate(search_result):
            print(str(val) + ": " + res)
        id_movie = input('ID do filme: ')
        return movies_db.get(search_result[int(id_movie)])
    elif len(search_result) == 1:
        return movies_db.get(search_result[0])
    else:
        return ''

def along_script_sent(full_script):
    """Realiza um gráfico com os valores do sentimento
       ao longo do filme passado por argumento."""
    num_blocks = 500
    block_scores = []
    block_size = int(len(full_script) / num_blocks)
    nltk_sentiment = SentimentIntensityAnalyzer()
    for i in range(num_blocks-1):
      curr_block = full_script[i*block_size:(i+1)*block_size]
      block_score = nltk_sentiment.polarity_scores(curr_block)
      block_scores.append(block_score.get('compound'))
    curr_block = full_script[i*block_size:]
    block_score = nltk_sentiment.polarity_scores(curr_block)
    block_scores.append(block_score.get('compound'))

    x = np.arange(0, num_blocks)
    y = block_scores
    plt.scatter(x, y)
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x, p(x), "r--")
    plt.ylabel('< negativo ---- positivo >')
    plt.show()


def get_characters(url):
    """Dado um url de um filme do site IMSDb,
       devolve um dicionário em que a chave é o
       nome de uma personagem e o valor é uma lista
       com as falas dessa personagem."""
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    full_script = ''
    chars = set()
    for child in soup.pre.children:
        if not re.match(r'<b>\s*TRANSITION:?\n</b>', str(child)):
            # Nome das personagens
            match = re.search(r'<b>\s+[a-zA-Z0-9]+(( [a-zA-Z0-9]+)?){,2}(\s*\(.*\))?\s*\n(</b>)?', str(child))
            if match:
                name = child.string.strip()
                name = re.sub(r'\s*\(.*\)', '', name)
                chars.add(name)
    return chars

def scrap_full_script(url):
    """Obtém o script de um filme dado o seu url."""
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    full_script = ''
    for child in soup.pre.children:
        if not re.search(r'<b>', str(child)):
            full_script += child.string
    return full_script

def cleaning_data(text):
    """Realiza o tratamento dos dados."""
    text = text.lower()
    text = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', text)
    text = re.sub(r'\w*\d\w*', ' ', text)
    text = re.sub(r'[‘’“”…]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def info_movie(url):
    """Imprime para o ecrã um pequeno sumário do filme
       dado pelo argumento url"""
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    print('Título: ' + soup.find('h1').contents[0])
    info = soup.find('div', class_='subtext')
    print('Restrição de idade: ' + info.contents[0].strip())
    try: print('Duração: ' + info.time.string.strip())
    except AttributeError: pass
    print('Géneros: ' + ', '.join([g.string for g in info.findAll('a')[:-1]]))
    print('Data de estreia: ' + info.findAll('a')[-1].string)


if '-b' in ops:
    build()

if '-s' in ops:
    movie = input('Nome do filme: ')
    ia = IMDb()
    results = ia.search_movie(movie)
    mv = results[0]
    URL = ia.get_imdbURL(mv)
    info_movie(URL)

if '-a' in ops:
    movies_db = build_movies_db()
    choosen_movie = get_movie_url(movies_db)
    if choosen_movie:
        FULL_SCRIPT = scrap_full_script(choosen_movie)
        FULL_SCRIPT_CLEAN = cleaning_data(FULL_SCRIPT)
        along_script_sent(FULL_SCRIPT_CLEAN)
    else:
        print('Não foram encontrados resultados.')

if '-c' in ops:
    movies_db = build_movies_db()
    choosen_movie = get_movie_url(movies_db)
    if choosen_movie:
        CHARS = get_characters(choosen_movie)
        if CHARS:
            for char in sorted(CHARS):
                print(char)
        else:
            print('Não foram encontradas personagens.')
    else:
        print('Não foram encontrados resultados.')

if '-h' in ops:
    print("""Uso: python bs.py [OPTION]
Opções:
    -b      Permite carregar todos os filmes do site IMSDb.
    -a      Permite analisar o sentimento ao longo de um filme. Só pode ser usada depois da opção -b.
    -s      Permite pesquisar informações sobre um dado filme.
    -c      Permite listar as personagens de um dado filme. Só pode ser usada depois da opção -b.""")

