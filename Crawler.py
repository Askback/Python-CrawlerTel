import re
import threading

import requests
from bs4 import BeautifulSoup


DOMAIN = "https://django-anuncios.solyd.com.br"
URL_AUTO = "https://django-anuncios.solyd.com.br/automoveis/"
LINKS = []
TELEFONES = []


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
    try:
        cards_pai = soup.find("div", class_="ui three doubling link cards")
        cards = cards_pai.find_all("a")
    except Exception as e:
        print("Erro ao encontrar links", e)
        return None

    links = []
    for card in cards:
        try:
            link = card['href']
            links.append(link)
        except:
            pass

    return links


def encontrar_telefone(soup):
    try:
        descricao = soup.find_all("div", class_="sixteen wide column")[2].p.get_text().strip()
    except Exception as e:
        print("Erro ao encontrar telefones", e)
        return None

    regex = re.findall(r"\(?0?([1-9]{2})[ \-\.\)]{0,2}(9[ \-\.]?\d{4})[ \-\.]?(\d{4})", descricao)
    if regex:
        return regex


def descobrir_telefone():
    while len(LINKS) != 0:
        link_anuncio = LINKS.pop(0)

        resposta_anuncio = buscar(DOMAIN + link_anuncio)

        if resposta_anuncio:
            soup_anuncio = parsing(resposta_anuncio)
            if soup_anuncio:
                telefones = encontrar_telefone(soup_anuncio)
                if telefones:
                    for telefone in telefones:
                        print("Telefone encontrado:", telefone)
                        TELEFONES.append(telefone)


if __name__ == "__main__":
    resposta_busca = buscar(DOMAIN)
    if resposta_busca:
        soup_busca = parsing(resposta_busca)
        if soup_busca:
            LINKS = encontrar_links(soup_busca)

            thread_1 = threading.Thread(target=descobrir_telefone)
            thread_2 = threading.Thread(target=descobrir_telefone)
            thread_3 = threading.Thread(target=descobrir_telefone)

            thread_1.start()
            thread_2.start()
            thread_3.start()

            thread_1.join()
            thread_2.join()
            thread_3.join()

            print(TELEFONES)



