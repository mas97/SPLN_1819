#! /usr/bin/env python3

import sys
import getopt
import requests
import re
import string
import matplotlib.pyplot as plt
import numpy as np
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from sklearn.feature_extraction import text
from wordcloud import WordCloud

opts, args = getopt.getopt(sys.argv[1:], 'bpftac:')
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

# Score do filme ao longo do tempo
def along_char_sent(full_char_script):
    N = 60
    block_scores = []
    total = len(full_char_script)
    block_size = int(len(full_char_script) / N)
    nltk_sentiment = SentimentIntensityAnalyzer()
    for i in range(N-1):
        block_score = nltk_sentiment.polarity_scores(full_char_script[i*block_size:(i+1)*block_size])
        block_scores.append(block_score.get('compound'))
    block_score = nltk_sentiment.polarity_scores(full_char_script[i*block_size:])
    block_scores.append(block_score.get('compound'))

    x = np.arange(0, N)
    y = block_scores

    fit = np.polyfit(x, y, 1)
    fit_fn = np.poly1d(fit)

    plt.plot(x, y, 'yo', x, fit_fn(x), '--k')
    plt.ylabel('< negativo ---- positivo >')
    plt.show()

# Score do filme
def full_script_sent(full_script):
    nltk_sentiment = SentimentIntensityAnalyzer()
    full_movie_score = nltk_sentiment.polarity_scores(full_script)
    print(full_movie_score)

# Score do filme ao longo do tempo

def along_script_sent(full_script):
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

    fit = np.polyfit(x, y, 1)
    fit_fn = np.poly1d(fit)

    plt.plot(x, y, 'yo', x, fit_fn(x), '--k')
    plt.ylabel('< negativo ---- positivo >')
    plt.show()


def scrap_titanic_():
    page = requests.get("https://www.imsdb.com/scripts/Titanic.html")
    soup = BeautifulSoup(page.text, "html.parser")
    full_script = ''
    pers = dict()
    name = None
    for child in soup.pre.children:
        if not re.match(r'<b>\s*TRANSITION:?\n</b>', str(child)):
            # Nome das personagens
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
        else:
            name = None
    return full_script, pers

def scrap_titanic():
    page = requests.get("https://www.imsdb.com/scripts/Titanic.html")
    soup = BeautifulSoup(page.text, "html.parser")
    full_script = ''
    for child in soup.pre.children:
        if not re.search(r'<b>', str(child)):
            full_script += child.string
    return full_script

def cleaning_data(text):
    text = text.lower()
    text = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', text)
    text = re.sub(r'\w*\d\w*', ' ', text)
    text = re.sub(r'[‘’“”…]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def top_words(block_script, chars, prefix):
    chars_names = [c.lower() for c in chars.keys()]
    stopwords = set()
    top_dict = dict()
    for w in block_script.split():
        if w in text.ENGLISH_STOP_WORDS or len(w) < 3 or w in chars_names:
            stopwords.update([w])
        elif w in top_dict:
            top_dict[w] += 1
        else:
            top_dict[w] = 1
    sorted_top = sorted(top_dict.items(), key=lambda x: x[1])
    for w in sorted_top[-5:]:
        stopwords.update([w[0]])
    wc = WordCloud(stopwords=stopwords, background_color="white", colormap="Dark2", max_font_size=150, random_state=42, width=1000, height=600)
    wordcloud = wc.generate(block_script)
    wordcloud.to_file(prefix + "_block.png")
    # plt.imshow(wordcloud, interpolation='bilinear')
    # plt.axis("off")
    # plt.show()



if '-b' in ops:
    build()
if '-p' in ops:
    FULL_SCRIPT, CHARS = scrap_titanic_()
    for k, v in CHARS.items():
        CHARS[k] = cleaning_data(''.join(v))
    scores_pers(CHARS)
if '-f' in ops:
    FULL_SCRIPT, CHARS = scrap_titanic_()
    FULL_SCRIPT_CLEAN = cleaning_data(FULL_SCRIPT)
    full_script_sent(FULL_SCRIPT_CLEAN)
if '-t' in ops:
    FULL_SCRIPT, CHARS = scrap_titanic_()
    FULL_SCRIPT_CLEAN = cleaning_data(FULL_SCRIPT)
    num_blocks = 3
    block_size = int(len(FULL_SCRIPT_CLEAN) / num_blocks)
    for i in range(num_blocks-1):
        curr_block = FULL_SCRIPT_CLEAN[i*block_size:(i+1)*block_size]
        top_words(curr_block, CHARS, str(i))
    curr_block = FULL_SCRIPT_CLEAN[i*block_size:]
    top_words(curr_block, CHARS, str(i+1))
if '-a' in ops:
    FULL_SCRIPT = scrap_titanic()
    FULL_SCRIPT_CLEAN = cleaning_data(FULL_SCRIPT)
    along_script_sent(FULL_SCRIPT_CLEAN)
if '-c' in ops:
    FULL_SCRIPT, CHARS = scrap_titanic_()
    CHARS_TEXT = ''.join(CHARS[ops.get('-c')])
    CHARS_CLEAN = cleaning_data(CHARS_TEXT)
    along_char_sent(CHARS_CLEAN)
