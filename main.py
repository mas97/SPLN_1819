#import periodictable as pt
import sys
import fileinput
import re
import itertools
from tree import *
import os
import getopt
import threading

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
            nthreads = int(arg)
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

    #Array with words represented by elements
    elements = []

    # process_words(input, output)
    threadLock = threading.Lock()
    threads = []

    for i in range(0,nthreads):
        # Create new thread
        threadI = myThread(i, input, output, threadLock, elements)
        # Add thread to thread list
        threads.append(threadI)

    # Start new Threads
    for t in threads:
       t.start()

    # Wait for all threads to complete
    for t in threads:
       t.join()

    pretty_print(elements, output)

class myThread (threading.Thread):
    def __init__(self, threadID, input, output, threadLock, elements):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.input = input
        self.output = output
        self.threadLock = threadLock
        self.elements = elements
    def run(self):
        process_words(self.input, self.output, self.threadLock, self.elements)

def process_words(input, output, threadLock, elements):
    line = input.readline()
    line = line.rstrip()
    while(line != ''):
        root = Node("root", line) # não me interessa o elemento da raiz chamei-lhe root
        root.create(line[0],line[1:]) # chama a função create que vai construir recursivamente a arvore a partir do nodo raiz root
        collectElems = []
        root.SearchTree(elements, collectElems, threadLock)
        line = input.readline()
        line = line.rstrip()

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

main()
