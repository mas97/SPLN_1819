#import periodictable as pt
import sys
import fileinput
import re
import itertools
from tree import *
import os
import getopt

def main():
    inputfile = ''
    outputfile = ''
    try: 
        opts, args = getopt.getopt(sys.argv[1:],"i:o:hv",["ifile=","ofile=","help=","version="])
    except getopt.GetoptError:
        print('main.py [-i <inputfile>] [-o <outputfile>]')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('main.py [-i <inputfile>] [-o <outputfile>]')
            sys.exit()
        elif opt in ('-v', '--version'):
            print('Version 1.0')
            sys.exit()
        elif opt in ('-i', '--ifile'):
            inputfile = arg
        elif opt in ('-o', '--ofile'):
            outputfile = arg

    # input from STDIN or file
    if inputfile != '':
        input = open(inputfile, 'r')
    else:
        input = sys.stdin
    # output to STDOUT or file
    if outputfile != '':
        output = open(outputfile, 'w+')
    else:
        output = sys.stdout

    process_words(input, output)


def process_words(input, output):
    line = input.readline()
    while(line != ''):
        line = line.rstrip()
        root = Node("root", line) # não me interessa o elemento da raiz chamei-lhe root
        root.create(line[0],line[1:]) # chama a função create que vai construir recursivamente a arvore a partir do nodo raiz root
        elements = []
        collectElems = []
        root.SearchTree(elements, collectElems)
        pretty_print(elements, output)
        line = input.readline()

def pretty_print(elements, output):
    #Para não ter uma ',' antes do primeiro simbolo no output
    first = True 

    #Para não ter uma ';' no final da linha
    last = False 

    for e in elements:
        #Caso tenha acabado um conjunto de 
        #simbolos e vai começar outro
        if (e != '!' and first and last): 
            print(';' + e, end='', file=output)
            first = False
            last = False
        #Caso seja o primeiro não mete ','
        elif (e != '!' and first): 
            print(e, end='', file=output)
            first = False
        #Caso não seja o primeiro então mete ',' antes
        elif (e != '!'):
            print(',' + e, end='', file=output)
        #Se chegou ao fim pede para meter ';'
        else:
            first = True
            last = True

    #Muda de linha para imprimir os resultados de outra palavra
    print('', file=output)

main()
