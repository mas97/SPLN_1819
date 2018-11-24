#! /usr/bin/env python3

import sys
import getopt
import requests
import re
import matplotlib.pyplot as plt
import numpy as np
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer

opts, args = getopt.getopt(sys.argv[1:], 'bpfa')
ops = dict(opts)

def build():
    """Coloca em ficheiro todos os filmes presentes no site: www.imsdb.com"""

    alphabet = "0ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    names_pages = []

    #reunião de todas as páginas de nomes de filmes
    for i in range(0, 27):
        print("Getting " + "https://www.imsdb.com/alphabetical/" + alphabet[i])
        request = requests.get("https://www.imsdb.com/alphabetical/" + alphabet[i])
        names_pages.append(request)
    res = ""
    for page in names_pages:
        html = page.text
        page_soup = BeautifulSoup(html, "html.parser")
        results = page_soup.find_all('a')
        aux = []
        for result in results:
            if len(result.attrs) == 2 and result.text != "":
                aux.append(result.text)
        aux = aux[:-5]
        for name in aux:
            name = name.replace(' ', '-')
            name = name.replace(':', '')
            res = res + 'https://www.imsdb.com/scripts/' + name + '.html' + '\n'
    file = open("films_names", "w")
    file.write(res)
    file.close()

# Scores por personagem
def scores_pers(characters):
    scores = []
    for k in characters.keys():
        speech = ''
        for sent in characters[k]:
            speech += sent
        nltk_sentiment = SentimentIntensityAnalyzer()
        score = nltk_sentiment.polarity_scores(speech)
        scores.append((k, str(score.get('compound'))))

    sorted_scores = sorted(scores, key=lambda x: x[1])
    for (char, score) in sorted_scores:
        print(char + ': ' + score)

# Score do filme
def full_script_sent(full_script):
    nltk_sentiment = SentimentIntensityAnalyzer()
    full_movie_score = nltk_sentiment.polarity_scores(full_script)
    print(full_movie_score)

# Score do filme ao longo do tempo
def along_script_sent(full_script):
    N = 500
    block_scores = []
    total = len(full_script)
    block_size = int(len(full_script) / N)
    nltk_sentiment = SentimentIntensityAnalyzer()
    for i in range(N-1):
        block_score = nltk_sentiment.polarity_scores(full_script[i*block_size:(i+1)*block_size])
        block_scores.append(block_score.get('compound'))
    block_score = nltk_sentiment.polarity_scores(full_script[i*block_size:])
    block_scores.append(block_score.get('compound'))

    x = np.arange(0, N)
    y = block_scores

    fit = np.polyfit(x, y, 1)
    fit_fn = np.poly1d(fit)

    plt.plot(x, y, 'yo', x, fit_fn(x), '--k')
    plt.ylabel('< negativo ---- positivo >')
    plt.show()


def scrap_titanic():
    PAGE = requests.get("https://www.imsdb.com/scripts/Titanic.html")
    PAGE_TEXT = PAGE.text
    SOUP = BeautifulSoup(PAGE_TEXT, "html.parser")

    full_script = ''
    pers = dict()
    name = None
    for child in SOUP.pre.children:
        # Nome das personagens
        if not re.match('<b>\s*TRANSITION:?\n</b>', str(child)):
            if re.search(r'<b>\s+\w+(\s*\(.*\))?\n', str(child)):
                name = child.string.strip()
                name = re.sub(r'\s*\(.*\)', '', name)
                if not name in pers:
                    pers[name] = []
            # Tag das cenas
            elif re.match(r'<b>\w+', str(child)):
                name = None
            # Tag da direita
            elif re.search(r'\s+\w+:\n</b>', str(child)):
                name = None
            elif name:
                full_script += child.string
                pers[name].append(child.string)
            else:
                full_script += child.string
        # Quando for TRANSITION
        else:
            name = None

    return full_script, pers

if '-b' in ops:
    build()
if '-p' in ops:
    full_script, chars = scrap_titanic()
    scores_pers(chars)
if '-f' in ops:
    full_script, chars = scrap_titanic()
    full_script_sent(full_script)
if '-a' in ops:
    full_script, chars = scrap_titanic()
    along_script_sent(full_script)
