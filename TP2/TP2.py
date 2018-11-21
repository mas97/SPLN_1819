import sys
import getopt
import requests
from bs4 import BeautifulSoup

opts, args = getopt.getopt(sys.argv[1:], 'bto')
ops = dict(opts)

def build():
    alphabet = "0ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    names_pages = []

    #reunião de todas as páginas de nomes de filmes
    for i in range(0,27):
        print("Getting " + "https://www.imsdb.com/alphabetical/" + alphabet[i])
        request = requests.get("https://www.imsdb.com/alphabetical/" + alphabet[i])
        names_pages.append(request)
    res = ""
    for page in names_pages:
        html = page.text
        page_soup = BeautifulSoup(html, "html.parser")
        results = page_soup.find_all('a')
        aux = []
        for result in results :
            if len(result.attrs) == 2 and result.text != "":
                aux.append(result.text)
        aux = aux[:-5]
        for name in aux:
            name = name.replace(' ', '-')
            name = name.replace(':', '')
            res = res + 'https://www.imsdb.com/scripts/' + name + '.html' + '\n'
    
    f = open("films_names", "w")
    f.write(res)

page = requests.get("https://www.imsdb.com/scripts/Titanic.html")
page_text = page.text

soup = BeautifulSoup(page_text, "html.parser")

# EXTRAÇÃO APENAS DA ZONA QUE CONTEM OS NOMES DE PERSONAGENS E AS RESPETIVAS FALAS
for child in soup.pre.children:
    print(child)

if '-b' in ops:
    build()