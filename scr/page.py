from urllib.parse import ParseResult, urlparse
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import urllib.request as t
import json


def clear_data(str): # avoir la data sans les html tags 
    clear_projet = []
    for e, projet in enumerate(str):
        clear_projet.append(str[e].text)
    return clear_projet


def get(exemple, int):
    page = t.urlopen(exemple, timeout=20)
    source = bs(page, "html.parser")
    V = source.find_all('span', {'class': 's-post-summary--stats-item-number'})  # nombre de vues
    Pseudo = source.find_all('div', {'class': 's-user-card--link d-flex gs4'})   # Pseudo
    AllTitle = source.find_all('a', {'class': 's-link'})  # titre
    AllTitle.pop(0)    # .pop nous permet de retirer des strings du slice ici on supprime les 2 premiers et le dernier car ils sont vides
    AllTitle.pop(0)
    AllTitle.pop(50)
    Views = clear_data(V)
    titre = clear_data(AllTitle)
    Nom = clear_data(Pseudo)
    new_list = [s.replace("\n", "") for s in Nom]  #supprimer les \n du pseudo
    with open('page_' + str(int) + '.json', "w", encoding="utf-8") as f:
        for taille, contenus in enumerate(AllTitle):
            href = contenus['href']   #href du post
            href_titre = "https://stackoverflow.com" + str(href)
            page1 = t.urlopen(href_titre, timeout=20)
            question = bs(page1,"html.parser")
            tout = question.find_all('div', {'class': 's-prose js-post-body'})
            contenu_href = clear_data(tout)
            new_list1 = [s.replace("\n", "") for s in contenu_href]
            dictionary = {'nombre de vues' : Views[taille],'Pseudo': new_list[taille],'href': href,'contenus':new_list1,'titre': titre[taille], 'number': taille + 1}
            json.dump(dictionary, f, ensure_ascii=False, indent=4)


def scrape():
    page = 0
    while page < 5:
        page += 1
        print(page)
        link = "https://stackoverflow.com/questions?tab=newest&page=" + str(page)
        print(link)
        get(link, page)
        if page == 5:
            print("Scrap_Over")
            exit()


def allurl(name):
    reqs = requests.get(name)
    soup = bs(reqs.text, 'html.parser')

    urls = []
    for link in soup.find_all('a', href=True):
        print(link.get('href'))