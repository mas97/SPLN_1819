#! /usr/bin/env python3

import json
import requests
from tf_idf import match
from scraping import load_obj
from difflib import SequenceMatcher

# Quota: 300
access_key = '329367-Sugestão-E0OVQYJW'

TRUE_POSITIVE = 0
FALSE_POSITIVE = 0
FALSE_NEGATIVE = 0

def load_available_movies():
    """Carrega a lista de filmes disponíveis."""
    print('Loading available movies...')
    try:
        words_from_movies = load_obj('dict_movies_list_words')
        return list(words_from_movies.keys())
    except:
        print('ERROR - First use scrapping.py')
        exit(1)


def tastedive_suggested(title):
    """Extrai a lista de filmes sugeridos pelo site Tastedive
       para um certo filme."""
    suggested_movies = []
    request = requests.get('https://tastedive.com/api/similar?q=%22movie:' +\
                           title + '%22&type=movies&limit=10&k=' + access_key)
    td_data = json.loads(request.text)
    for movie_entry in td_data['Similar']['Results']:
        suggested_movies.append(movie_entry['Name'].lower())
    return suggested_movies


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def calc_now_true_positive(control, testing):
    now_true_positive = 0
    for title_testing in testing:
        print(title_testing)
        for title_control in control:
            if similar(title_testing, title_control.lower()) >= 0.8:
                now_true_positive += 1
                break
    return now_true_positive


def update_values(control, testing):
    """Atualiza os valores TRUE_POSITIVE e FALSE_POSITIVE"""
    global TRUE_POSITIVE, FALSE_POSITIVE, FALSE_NEGATIVE
    now_true_positive = calc_now_true_positive(control, testing)
    TRUE_POSITIVE += now_true_positive
    FALSE_NEGATIVE += len(control) - now_true_positive
    FALSE_POSITIVE += len(testing) - now_true_positive


def test_suggest_engine_precision(movies):
    """Compara os resultados entre o motor de sugestão desenvolvido
       e as sugestões do site tastedive"""
    for movie in movies[0:250]:
        print('Processing ' + movie)
        control = tastedive_suggested(movie)
        testing = [m[0] for m in match(movie)]
        if control and testing:
            update_values(control, testing)
    print('True positive: ' + str(TRUE_POSITIVE))
    print('False positive: ' + str(FALSE_POSITIVE))
    print('False negative: ' + str(FALSE_NEGATIVE))


def calc_precision(true_positive, false_positive):
    """Calcula a precisão."""
    return true_positive / (true_positive + false_positive)


def calc_recall(true_positive, false_negative):
    """Calcula o recall."""
    return true_positive / (true_positive + false_negative)


def calc_f1(precision, recall):
    """Calcula o f1 score."""
    return 2 * ((precision * recall) / (precision + recall))


MOVIES = load_available_movies()
test_suggest_engine_precision(MOVIES)
