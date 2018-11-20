import requests
from bs4 import BeautifulSoup

page = requests.get("https://www.imsdb.com/scripts/Titanic.html")
page_text = page.text

soup = BeautifulSoup(page_text, "html.parser")

# EXTRAÇÃO APENAS DA ZONA QUE CONTEM OS NOMES DE PERSONAGENS E AS RESPETIVAS FALAS
for child in soup.pre.children:
    print(child)