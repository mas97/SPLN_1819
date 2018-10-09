#import periodictable as pt
import sys
import fileinput
import re
import itertools
from tree import *
import os
import getopt
import threading
import queue
import codecs
import datetime

def main():
    inputfile = ''
    outputfile = ''
    nthreads = 1
    try: 
        opts, args = getopt.getopt(sys.argv[1:],"t:i:o:hv",["threads=","ifile=","ofile=","help=","version="])
    except getopt.GetoptError:
        print('main.py [-i <inputfile>] [-o <outputfile>] [-t <num threads>]')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('main.py [-i <inputfile>] [-o <outputfile>] [-t <num threads>]')
            sys.exit()
        elif opt in ('-v', '--version'):
            print('Version 1.0')
            sys.exit()
        elif opt in ('-t', '--threads'):
            # nthreads = int(arg)
            print('The Thread feature is disabled for the moment.')
            sys.exit()
        elif opt in ('-i', '--ifile'):
            inputfile = arg
        elif opt in ('-o', '--ofile'):
            outputfile = arg

    # input from STDIN or file
    if inputfile != '':
        input = codecs.open(inputfile, 'r', 'latin1')
    else:
        input = sys.stdin
    # output to STDOUT or file
    if outputfile != '':
        output = open(outputfile, 'w+')
    else:
        output = sys.stdout

    # Array with words represented by elements
    elements = {}

    # Create queue
    q = queue.Queue()

    # Create new thread
    t = myThread(input, elements, q)
    t.setDaemon(True)

    # Start new Thread
    t.start()

    for rawLine in input:
        # m = re.search(r'\t(.+$)', rawLine)
        # if m is not None:
            # line = m.group(1)
            # if (line != ''):
                # #Put line to queue
                # q.put(line)
        rawLine = rawLine.rstrip()
        q.put(rawLine)

    #wait on the queue until everything has been processed 
    q.join()

    # Close de queue
    q.put(None)

    # Wait for all threads to complete
    t.join()
    # print(elements['pouco'])
    pretty_print(elements, output)
    WriteFile("index.html", elements)

class myThread (threading.Thread):
    def __init__(self, input, elements, q):
        threading.Thread.__init__(self)
        self.input = input
        self.elements = elements
        self.q = q
    def run(self):
        while True:
            line = self.q.get()
            if line is None:
                break
            process_words(line, self.input, self.elements)
            self.q.task_done()

def process_words(line, input, elements):
    if(line != ''):
        root = Node("root", line, line) # não me interessa o elemento da raiz chamei-lhe root
        root.create(line[0],line[1:], line) # chama a função create que vai construir recursivamente a arvore a partir do nodo raiz root
        collectElems = []
        root.SearchTree(elements, collectElems)

def pretty_print(elements, output):
    #Para não ter uma ',' antes do primeiro simbolo no output
    first = True 

    #Para não ter uma ';' no final da linha
    last = False 

    for e in elements:
        #Caso tenha acabado um conjunto de 
        #simbolos e vai começar outro
        if (e != '!' and first and last): 
            print('\n' + e, end='', file=output)
            first = False
            last = False
        #Caso seja o primeiro não mete ','
        elif (e != '!' and first): 
            print(e, end='', file=output)
            first = False
        #Caso não seja o primeiro então mete ',' antes
        elif (e != '!'):
            print(',' + e, end='', file=output)
        #Se chegou ao fim pede para meter '\n' entre palavras
        else:
            first = True
            last = True

    #Newline no final
    print('', file=output)


def WriteFile(file_name, elements):
    fst_row = True
    file = open(file_name, "w")
    # escrita do cabeçalho do ficheiro html
    file.write("<!DOCTYPE html>\n<html>\n<head>\n<title>Chemical Elements</title>\n</head>\n<body>\n")

    # abertura da primeira div do tipo row
    # if len(elements) > 0:
        # file.write("<div class=\"row\">\n")
    
    ks = elements.keys();
    for k in ks:
        for elems in elements[k]:
            file.write("<div class=\"row\">\n")
            for e in elems:
                file.write("\t<td>\n")
                file.write("\t\t<img src=\"images/" + e + ".png\" alt=\"\" width=\"50\" height=\"50\">\n")
                file.write("\t</td>\n")
            file.write("</div>\n")
        # escrita do código html para a criação de uma nova row
        # if e == "!":
            # if fst_row:
                # file.write("<div class=\"row\">\n")
                # fst_row = False
            # else:
                # file.write("</div>\n")
                # file.write("<div class=\"row\">\n")
        # else:
            # # escrita do código html de abertura de uma row em html para o posicionamento de imagens
            # # uma row para cada palavra a representar
            # file.write("\t<td>\n")
            # file.write("\t\t<img src=\"images/" + e + ".png\" alt=\"\" width=\"50\" height=\"50\">\n")
            # file.write("\t</td>\n")
    
    # abertura da primeira div do tipo row VER ESTE CASO
    # if len(elements) > 0:
        # file.write("</div>\n")

    # escrita do fecho do ficheiro html
    file.write("</body>\n</html>")



main()
