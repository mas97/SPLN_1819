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
        input = codecs.open(inputfile, 'r', 'latin1')
    else:
        input = sys.stdin
    # output to STDOUT or file
    if outputfile != '':
        output = open(outputfile, 'w+')
    else:
        output = sys.stdout

    # Array with words represented by elements
    elements = []

    # process_words(input, output)
    threadLock = threading.Lock()
    threads = []

    # Create queue
    q = queue.Queue()

    for i in range(nthreads):
        # Create new thread
        t = myThread(input, threadLock, elements, q)
        t.setDaemon(True)
        # Add thread to thread list
        threads.append(t)

    # Start new Threads
    for t in threads:
       t.start()

    for rawLine in input:
        m = re.search(r'\t(.+$)', rawLine)
        if m is not None:
            line = m.group(1)
            if (line != ''):
                #Put line to queue
                q.put(line)

    #wait on the queue until everything has been processed 
    q.join()

    for i in range(nthreads):
        q.put(None)

    # Wait for all threads to complete
    for t in threads:
       t.join()

    pretty_print(elements, output)

class myThread (threading.Thread):
    def __init__(self, input, threadLock, elements, q):
        threading.Thread.__init__(self)
        self.input = input
        self.threadLock = threadLock
        self.elements = elements
        self.q = q
    def run(self):
        while True:
            line = self.q.get()
            # print(line)
            if line is None:
                break
            process_words(line, self.input, self.threadLock, self.elements)
            self.q.task_done()

def process_words(line, input, threadLock, elements):
    # line = ''
    # rawLine = input.readline()
    # if rawLine is not None:
        # m = re.search(r'\t(.+$)', rawLine)
        # if m is not None:
            # line = m.group(1)
    # line = line.rstrip()
    if(line != ''):
        root = Node("root", line) # não me interessa o elemento da raiz chamei-lhe root
        root.create(line[0],line[1:]) # chama a função create que vai construir recursivamente a arvore a partir do nodo raiz root
        collectElems = []
        root.SearchTree(elements, collectElems, threadLock)
        # line = ''
        # rawLine = input.readline()
        # if rawLine is not None:
            # m = re.search(r'\t(.+$)', rawLine)
            # if m is not None:
                # line = m.group(1)
        # line = line.rstrip()

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
