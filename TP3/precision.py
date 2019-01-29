#! /usr/bin/env python3

import requests
import json
from bs4 import BeautifulSoup
from pprint import pprint


# API access key: 329367-Sugestão-E0OVQYJW
# Quota: 300

def tastedive_suggested(title):
    """Extrai a lista de filmes sugeridos pelo site Tastedive
       para um certo filme."""
    suggested_movies = []
    request = requests.get("https://tastedive.com/api/similar?q=%22movie:" +\
                           title + "%22&type=movies&k=329367-Sugest%C3%A3o-E0OVQYJW")
    soup = BeautifulSoup(request.text, "html.parser")
    td_data = json.loads(soup.text)
    for movie_entry in td_data['Similar']['Results']:
        suggested_movies.append(movie_entry['Name'].lower())
    return suggested_movies


def calc_precision(control, testing):
    """Calcula a precisão."""
    true_positive = len(set(testing) & set(control))
    false_positive = len(testing) - true_positive # Está bem?!?!?
    precision = true_positive / (true_positive + false_positive)
    return precision

control = tastedive_suggested('into the wild')
pprint(control)
