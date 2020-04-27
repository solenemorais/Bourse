# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 15:17:45 2020

@author: solen
"""

#bibliothèque pour le web scraping
from bs4 import BeautifulSoup
import requests

#bibliothèque pour le timer
import time #--> si on utilise une boucle while et sleep

#le module threading permet d'exécuter lus portions de code en même temps
#à voir ce qui est mieux entre time et threading
#import threading

#module schedule --> plus propre je trouve
#import schedule
#s = sched.scheduler(time.time, time.sleep)

#start_time=time.time()
#définition d'une fonction pour pouvoir changer l'url plus facilement
def scraping_page(url):

    while True:
        #threading.Timer(10.0, scraping_page).start()
        page = requests.get(url, timeout=10)
        #timeout autorise l'arrêt d'une requête si jamais il n'y a pas de réponse du serveur,
        #permet d'éviter une attente infinie
        soup = BeautifulSoup(page.text, features="html.parser")
    
        #print the html content:
        #print(soup.prettify())
    
        element = soup.find('div', class_="c-faceplate__price").find('span', class_="c-instrument c-instrument--last").text
        print(element)
        #si on enlève le premier find sur la classe "c-faceplate__price" la précision du texte passe à deux chiffres
        #au lieu de 4 derrière la virgule, vas savoir pourquoi lol
        time.sleep(10.0)

url= "https://www.boursorama.com/cours/NFLX/"
scraping_page(url)
