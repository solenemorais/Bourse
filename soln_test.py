# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 15:17:45 2020

@author: solen
"""

#bibliothèques pour le web scraping
from bs4 import BeautifulSoup
import requests

#bibliothèques pour fichiers
import csv
import os.path

#bibliothèque pour tracer le graphique dans la console
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#autres bibliothèques utiles
import pandas as pd
import time
import datetime
import tkinter as tk

#---- TRACE THE GRAPH ---
"""
def plotting_empty_graph():
    plt.plot()
    plt.show()
    plt.close()
    
    plt.xticks(rotation = 90)
    plt.xlabel("Heures de prélevement")
    plt.ylabel('Cours (en $)')
    plt.title("Relevé du cours de Netflix")
"""    
    
#---- SCRAPING DE LA PAGE WEB ----
    #fonction permettant de récupérer la donnée sur la page web

def scraping_page(url):
    page = requests.get(url, timeout=10)
    #timeout autorise l'arrêt d'une requête si jamais il n'y a pas de réponse du serveur, permet d'éviter une attente infinie
    
    soup = BeautifulSoup(page.text, features="html.parser")
    
    element = soup.find('div', class_="c-faceplate__price").find('span', class_="c-instrument c-instrument--last").text
    
    print("Nouvelle valeur récupérée : ", element)
    #si on enlève le premier find sur la classe "c-faceplate__price" la précision du texte passe à deux chiffres
    #au lieu de 4 derrière la virgule, vas savoir pourquoi lol
    return(element)



#---- FILL CSV / ADD DATA----
def filling_csv (data):
    file_exists = os.path.isfile('scrape_data.csv')
    if file_exists :
        with open('scrape_data.csv', 'a+', newline="") as csv_file:
            fieldnames = ["Valeur", "Jour", "Heure"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=";")
            writer.writerow(data)
    else:
        #---- CREATE A NEW CSV ----
        with open('scrape_data.csv', 'w', newline="") as csv_file:
            fieldnames = ["Valeur", "Jour", "Heure"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            writer.writerow(data)


    
#---- TRACER THE DATA ----
def plotting_data():
    #---- READ THE CSV ----
    plt.style.use('fivethirtyeight')

    def animate(i):
        data = pd.read_csv('scrape_data.csv')
        x = data['Heure']
        y = data['Valeur']
        
        plt.clear()
                    
        plt.plot(x, y, label='Channel 1')
        
        plt.legend(loc='upper left')
        plt.tight_layout()

    ani = FuncAnimation(plt.gcf(), animate, interval=1000)
    
    plt.tight_layout()
    plt.show()

#---- FONCTION PRENICPALE ----
def main():
    url= "https://www.boursorama.com/cours/NFLX/"
    data = {"Valeur" : scraping_page(url), "Jour" : datetime.date.today(),
            "Heure" : datetime.datetime.now().time()}
    #filling_csv(data)
    
    
if __name__=="__main__":
    #plotting_empty_graph()
    plotting_data()
   # while True:
        #main()
        #time.sleep(2.0)


