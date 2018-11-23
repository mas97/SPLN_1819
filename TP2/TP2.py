#! /usr/bin/env python3

import sys
import getopt
import requests
import re
import nltk
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer

opts, args = getopt.getopt(sys.argv[1:], 'bto')
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

if '-b' in ops:
    build()





# RASCUNHO
# # page = requests.get("https://www.imsdb.com/scripts/Titanic.html")
# # page = requests.get("https://www.imsdb.com/scripts/12-Years-a-Slave.html")
# page = requests.get("https://www.imsdb.com/scripts/Coco.html")
# page_text = page.text

# soup = BeautifulSoup(page_text, "html.parser")

# # EXTRAÇÃO APENAS DA ZONA QUE CONTEM OS NOMES DE PERSONAGENS E AS RESPETIVAS FALAS
# pers = {}
# name = None
# for child in soup.pre.children:
    # # Nomes das personagens
    # if re.match(r'^<b>\s+.+[^:]</b>', str(child)):
        # name = re.sub(r'^<b>\s+(.+)[^:]</b>', r'\1', str(child))
        # if not name in pers:
            # pers[name] = []
    # # TAGS das cenas
    # elif re.match(r'^<b>\w+', str(child)):
        # name = None
    # # Tags à direita
    # elif re.match(r'<b>\s+.+:', str(child)):
        # name = None
    # elif name:
        # pers[name].append(child.string)
# # print(list(set(pers)))
    # #print(set(pers))
    # # for p in dist:
        # # print(p)
# #print(pers)

# for (k,v) in pers.items():
    # print(k)
# s = ''
# for sp in pers['MIGUEL']:
  # s += sp
# nltk_sentiment = SentimentIntensityAnalyzer()
# score = nltk_sentiment.polarity_scores(s)

# print(score)

