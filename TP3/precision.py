#! /usr/bin/env python3

from pprint import pprint
import json
from bs4 import BeautifulSoup
import requests
from tf_idf import match
from scraping import load_obj


# API access key: 329367-Sugestão-E0OVQYJW
# Quota: 300

TRUE_POSITIVE = 0
FALSE_POSITIVE = 0

def load_available_movies():
    """Carrega a lista de filmes disponíveis."""
    print('Loading available movies...')
    try:
        words_from_movies = load_obj('dict_movies_list_words')
        return list(words_from_movies.keys())
    except:
        print('ERROR - First run: ./scrapping.py -b')
        exit(1)


def tastedive_suggested(title):
    """Extrai a lista de filmes sugeridos pelo site Tastedive
       para um certo filme."""
    suggested_movies = []
    request = requests.get('https://tastedive.com/api/similar?q=%22movie:' +\
                           title + '%22&type=movies&k=329367-Sugest%C3%A3o-E0OVQYJW')
    soup = BeautifulSoup(request.text, 'html.parser')
    td_data = json.loads(soup.text)
    for movie_entry in td_data['Similar']['Results']:
        suggested_movies.append(movie_entry['Name'].lower())
    return suggested_movies


def update_values(control, testing):
    """Atualiza os valores TRUE_POSITIVE e FALSE_POSITIVE"""
    global TRUE_POSITIVE, FALSE_POSITIVE
    now_true_positive = len(set(testing) & set(control))
    TRUE_POSITIVE += now_true_positive
    FALSE_POSITIVE += len(testing) - now_true_positive # Está bem?!?!?


def calc_precision():
    """Calcula a precisão."""
    return TRUE_POSITIVE / (TRUE_POSITIVE + FALSE_POSITIVE)


def test_suggest_engine_precision(movies):
    """Compara os resultados entre o motor de sugestão desenvolvido
       e as sugestões do site tastedive"""
    for movie in movies[:200]:
        print('Processing ' + movie)
        control = tastedive_suggested(movie)
        testing = [m[0] for m in match(movie)]
        if control and testing:
            update_values(control, testing)
    print(TRUE_POSITIVE)
    print(FALSE_POSITIVE)


MOVIES = load_available_movies()
test_suggest_engine_precision(MOVIES)
