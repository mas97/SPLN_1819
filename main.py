import periodictable as pt
import sys
import fileinput
import re
import itertools
from tree import *
import os

#dá a lista dos elementos todos
#elements = str(pt.elements.list('symbol'))


# =========================== TABELA PERIODICA ===========================

tp = { 
    'h': 1,
    'he': 2,
    'li': 2,
    'be': 2,
    'b': 1,
    'c': 1,
    'n': 1,
    'o': 1,
    'f': 1,
    'ne': 2,
    'na': 2,
    'mg': 2,
    'al': 2,
    'si': 2,
    'p': 1,
    's': 1,
    'cl': 2,
    'ar': 2,
    'k': 1,
    'ca': 2,
    'sc': 2,
    'ti': 2,
    'v': 1,
    'cr': 2,
    'mn': 2,
    'fe': 2,
    'co': 2,
    'ni': 2,
    'cu': 2,
    'zn': 2,
    'ga': 2,
    'ge': 2,
    'as': 2,
    'se': 2,
    'br': 2,
    'kr': 2,
    'rb': 2,
    'sr': 2,
    'y': 1,
    'zr': 2,
    'nb': 2,
    'mo': 2,
    'tc': 2,
    'ru': 2,
    'rh': 2,
    'pd': 2,
    'ag': 2,
    'cd': 2,
    'in': 2,
    'sn': 2,
    'sb': 2,
    'te': 2,
    'i': 1,
    'xe': 2,
    'cs': 2,
    'ba': 2,
    'la': 2,
    'ce': 2,
    'pr': 2,
    'nd': 2,
    'pm': 2,
    'sm': 2,
    'eu': 2,
    'gd': 2,
    'tb': 2,
    'dy': 2,
    'ho': 2,
    'er': 2,
    'tm': 2,
    'yb': 2,
    'lu': 2,
    'hf': 2,
    'ta': 2,
    'w': 1,
    're': 2,
    'os': 2,
    'ir': 2,
    'pt': 2,
    'au': 2,
    'hg': 2,
    'tl': 2,
    'pb': 2,
    'bi': 2,
    'po': 2,
    'at': 2,
    'rn': 2,
    'fr': 2,
    'ra': 2,
    'ac': 2,
    'th': 2,
    'pa': 2,
    'u': 1,
    'np': 2,
    'pu': 2,
    'am': 2,
    'cm': 2,
    'bk': 2,
    'cf': 2,
    'es': 2,
    'fm': 2,
    'md': 2,
    'no': 2,
    'lr': 2,
    'rf': 2,
    'db': 2,
    'sg': 2,
    'bh': 2,
    'hs': 2,
    'mt': 2,
    'ds': 2,
    'rg': 2,
    'cn': 2,
    'nh': 2,
    'fl': 2,
    'mc': 2,
    'lv': 2,
    'ts': 2,
    'og': 2
}

# =========================== ******* ===========================

for line in fileinput.input():
    aux = line.rstrip()
    root = Node("root", aux) # não me interessa o elemento da raiz chamei-lhe root
    root.create(aux[0],aux[1:]) # chama a função create que vai construir recursivamente a arvore a partir do nodo raiz root
    #print(line.rstrip())
    print("ARVORE")
    root.PrintTree()
    print("fim de ciclo")

"""     match_elements = []
    permutations = []
    words = []

    for key, value in tp.items():
        if re.search(key, line):
            match_elements.append(key)
    
    #print(len(line))

    # -1 porque estou a subtrair o \n
    for i in range(1, len(line) - 1):
        aux = list(itertools.combinations(match_elements, i))
        if aux != []:
            permutations.append(aux)
    
    #print(permutations)
    
    length = 0

    for p in permutations:
        for e in p:
            print(e)
            length += tp[e]
        if length == len(line):
            words.append(line) """