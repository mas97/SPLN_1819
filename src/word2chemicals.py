import sys
import fileinput
import re
import itertools
from tree import *
from clean import *
import os
import getopt
import threading
import queue
import codecs
import datetime

def main():
    inputfile = ''
    outputfile = ''
    clean = ''
    cleanfile = ''
    try: 
        opts, args = getopt.getopt(sys.argv[1:],"f:c:i:o:hv",["cleanfile=","clean=","ifile=","ofile=","help=","version="])
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
        elif opt in ('-i', '--ifile'):
            inputfile = arg
        elif opt in ('-o', '--ofile'):
            outputfile = arg
        elif opt in ('-c', '--clean'):
            clean = arg
        elif opt in ('-f', '--cleanfile'):
            cleanfile = arg

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

    if cleanfile != '':
        fd = open(cleanfile, 'r')
        clean = fd.read()
        fd.close()

    # Dictionary
    # key   -> word
    # value -> array of arrays of elements
    elements = {}

    if inputfile == '':
        for rawLine in input:
            line = rawLine.rstrip()
            process_words(line, elements)
    elif clean != '':
        words = separate_cmds(input, clean)
        for word in words:
            process_words(word, elements)

    # Generate HTML file
    writeFile(output, elements)

    input.close()
    output.close()

def process_words(line, elements):
    if(line != ''):
        root = Node("root", line, line) 
        root.create(line[0],line[1:], line) 
        collectElems = []
        root.SearchTree(elements, collectElems)


def writeFile(output, elements):
    # escrita do cabeçalho do ficheiro html
    output.write("<!DOCTYPE html>\n<html>\n<head>\n<title>Chemical Elements</title>\n</head>\n<body>\n")

    ks = elements.keys()
    for k in ks:
        output.write("<h1>" + k + "</h1>")
        for elems in elements[k]:
            output.write("<div class=\"row\">\n")
            for e in elems:
                output.write("\t<td>\n")
                output.write("\t\t<img src=\"images/" + e + ".png\" alt=\"\" width=\"50\" height=\"50\">\n")
                output.write("\t</td>\n")
            output.write("</div>\n")
        output.write("<hr>")

    # escrita do fecho do ficheiro html
    output.write("</body>\n</html>")


# Execuçãoo
main()
