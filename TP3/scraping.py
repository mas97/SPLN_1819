#! /usr/bin/env python3

import time
import pickle
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

opts, args = getopt.getopt(sys.argv[1:], 'hbl')
ops = dict(opts)

def get_movies_url():
    """Coloca em ficheiro todos os filmes presentes no site: www.imsdb.com"""

    alphabet = "0ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    names_pages = []
    list_urls = []

    #reunião de todas as páginas de nomes de filmes
    for c in alphabet:
        print("Getting " + "https://www.imsdb.com/alphabetical/" + c)
        request = requests.get("https://www.imsdb.com/alphabetical/" + c)
        names_pages.append(request)
    for page in names_pages:
        page_soup = BeautifulSoup(page.text, "html.parser")
        results = page_soup.find_all('a')
        for result in results:
            if re.search(r'<p>', str(result.parent)) and 'href' in result.attrs and 'title' in result.attrs:
                title = result.text.replace(' ', '-')
                title = title.replace(':', '')
                url = 'https://www.imsdb.com/scripts/' + title + '.html' + '\n'
                list_urls.append(url.strip())
    return list_urls

def build_movies_db(list_urls):
    movies_db = dict()
    for url in list_urls:
        match = re.search(r'scripts/(.*?)\.html', url)
        if match:
            key = re.sub(r'-', r' ', match.group(1))
            key = key.lower()
            movies_db[key] = url.strip()
    return movies_db

def along_script_sent(title, full_script):
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
    plt.savefig('movies_sent_pict/' + title + '.png', bbox_inches='tight')
    plt.close()
    #plt.show()


def clean_script(text):
    text = text.replace('Back to IMSDb', '')
    text = text.replace('''<b><!--
</b>if (window!= top)
top.location.href=location.href
<b>// -->
</b>
''', '')
    text = text.replace('''          Scanned by http://freemoviescripts.com
          Formatting by http://simplyscripts.home.att.net
''', '')
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = text.lower()
    text = text.replace(r'\r', '')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def scrap_full_script(url):
    """Obtém o script de um filme dado o seu url."""
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    full_script = soup.find_all('td', {'class': "scrtext"})[0].get_text()
    return clean_script(full_script)

def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as fp:
        pickle.dump(obj, fp, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name + '.pkl', 'rb') as fp:
        return pickle.load(fp)

def fix_title(title):
    match = re.search(r',-The$', title)
    if match:
        title = re.sub(r',-The$', '', title)
        title = 'the ' + title
    title = re.sub(r'-', ' ', title)
    return title.lower()

def save_full_scripts(list_urls):
    words_from_movies = {}
    genres_from_movies = {}
    IMDb_access = IMDb()
    size = len(list_urls)
    for i, url in enumerate(list_urls, start=1):
        time.sleep(1)
        try:
            full_script = scrap_full_script(url)
            match = re.search(r'scripts/(.*?)\.html', url)
            if match:
                title = fix_title(match.group(1))
                if len(full_script) > 100:
                    along_script_sent(title, full_script)
                    # Map: title -> list of words
                    words_from_movies[title] = full_script
                    # Map: title -> list of genres
                    movies = IMDb_access.search_movie(title)
                    movie_infos = IMDb_access.get_movie(movies[0].getID())
                    genres_from_movies[title] = movie_infos['genre']
                    print('[' + str(i) + '/' + str(size) + '] ' + title)
                else:
                    print('[' + str(i) + '/' + str(size) + '] ' + title + ' [SMALL SCRIPT]')
            else:
                print('[' + str(i) + '/' + str(size) + '] ' + title + ' [PARSING ERROR]')
        except IndexError:
            match = re.search(r'scripts/(.*?)\.html', url)
            title = fix_title(match.group(1))
            print('[' + str(i) + '/' + str(size) + '] ' + title + ' [NO SCRIPT]')
    print('Saving words_from_movies to file...')
    save_obj(words_from_movies, 'dict_movies_list_words')
    print('Saving genres_from_movies to file...')
    save_obj(genres_from_movies, 'dict_movies_list_genres')

if '-b' in ops:
    list_urls = get_movies_url()
    save_full_scripts(list_urls)
    print('Done!')

if '-l' in ops:
    words_from_movies = load_obj('dict_movies_list_words')
    # fazer coisas com o dicionário

if '-h' in ops:
    print("""Uso: python bs.py [OPTION]
Opções:
    -b      Permite carregar todos os filmes do site IMSDb.
    -a      Permite analisar o sentimento ao longo de um filme. Só pode ser usada depois da opção -b.
    -s      Permite pesquisar informações sobre um dado filme.
    -c      Permite listar as personagens de um dado filme. Só pode ser usada depois da opção -b.""")

