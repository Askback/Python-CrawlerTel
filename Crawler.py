import requests
from bs4 import BeautifulSoup

DOMAIN = "ttps://django-anuncios.solyd.com.br"
URL_AUTO = "https://django-anuncios.solyd.com.br/automoveis/"


def buscar(url):
    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            return resposta.text
        else:
            print("Erro ao processar está requisição")
    except Exception as e:
        print("Erro ao fazer a requisição", e)


def parsing(resposta_html):
    try:
        soup = BeautifulSoup(resposta_html, 'html.parser')
        return soup
    except Exception as e:
        print("Erro ao fazer o parsing", e)


def encontrar_links(soup):
    cards_pai = soup.find("div", class_="ui three doubling link cards")
    cards = cards_pai.find_all("a")

    links = []
    for card in cards:
        link = card['href']
        links.append(link)

    return links


resposta = buscar(URL_AUTO)
if resposta:
    soup = parsing(resposta)
    if soup:
        links = encontrar_links(soup)
        print(links)
