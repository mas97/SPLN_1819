import periodictable as pt
import sys
import fileinput
import re
import itertools
from tree import *
import os

#dá a lista dos elementos todos
#elements = str(pt.elements.list('symbol'))

for line in fileinput.input():
    aux = line.rstrip()
    root = Node("root", aux) # não me interessa o elemento da raiz chamei-lhe root
    root.create(aux[0],aux[1:]) # chama a função create que vai construir recursivamente a arvore a partir do nodo raiz root
    #print(line.rstrip())
    #print("ARVORE")
    #root.PrintTree()
    #print("fim de ciclo")
    elements = []
    root.SearchTree(elements)
    print(elements)

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