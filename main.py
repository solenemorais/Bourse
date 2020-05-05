# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 17:27:00 2020

@author: Aurélien
"""

#Ce fichier sera le main du coup faudra pas changer le nom dans le différentes branche pour qu'on puisse les fusionner après

#IMPORT
import time
from selenium import webdriver

#bibliothèques pour fichiers
import csv
import os.path

#bibliothèque pour tracer le graphique dans la console
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from numpy import array

#autres bibliothèques utiles
import pandas as pd
import time
from datetime import datetime
import tkinter as tk

#CONSTANTE
PAUSE=10

#VARIABLE
dataFrame=pd.DataFrame({'data':[],'time':[]})

#Ici on a les différentes fonctions qui font être exécutées en fonction de la monnaie choisis
def scrap(name,url):
    get_data_csv(name)
    driver=webdriver.Firefox()
    driver.get(url)
    while(True):
        price=driver.find_element_by_id("price-ticker").find_elements_by_tag_name('span')[1]
        dataFrame.loc[dataFrame.shape[0]]=[float(price.text[:-4]),datetime.now()]
        filling_csv(name,dataFrame)
        time.sleep(PAUSE)

def get_data_csv(name):
    filename=str(name+'.csv')
    file_exists = os.path.isfile(filename)
    if file_exists :
        dataFrame=pd.read_csv('scrape_data.csv',sep="/")

def filling_csv (name,df):
    filename=str(name+'.csv')
    file_exists = os.path.isfile(filename)
    if file_exists :
        with open(filename, 'a+', newline="") as csv_file:
            fieldnames = ["Valeur", "Date"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter="/")
            for row in df.itertuples() :
                writer.writerow({"Valeur" : row.data, "Date" : row.time})
    else:
        #---- CREATE A NEW CSV ----
        with open(filename, 'w', newline="") as csv_file:
            fieldnames = ["Valeur", "Date"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter="/")
            writer.writeheader()
            for row in df.itertuples() :
                writer.writerow({"Valeur" : row.data, "Date" : row.time})
            
#ici en fonction de la monnaie choisie on va exécuter la fonction correspondante
#Par exemple ici si la monnaie est BTC on va exécuter la fonction BTC()    
monnaie="ETH"
if monnaie=="BTC":
    scrap(monnaie,'https://trade.kraken.com/fr-fr/charts/KRAKEN:BTC-EUR')
elif monnaie=="ETH":
    scrap(monnaie,'https://trade.kraken.com/fr-fr/charts/KRAKEN:ETH-EUR')
elif monnaie=="LTC":
    scrap(monnaie,'https://trade.kraken.com/fr-fr/charts/KRAKEN:LTC-EUR')
elif monnaie=="MON":
    scrap(monnaie,'https://trade.kraken.com/fr-fr/charts/KRAKEN:MLN-EUR')
elif monnaie=="EOS":
    scrap(monnaie,'https://trade.kraken.com/fr-fr/charts/KRAKEN:EOS-EUR')
elif monnaie=="CAR":
    scrap(monnaie,'https://trade.kraken.com/fr-fr/charts/KRAKEN:ATOM-EUR')
elif monnaie=="WAVE":
    scrap(monnaie,'https://trade.kraken.com/fr-fr/charts/KRAKEN:WAVES-EUR')
elif monnaie=="DASH":
    scrap(monnaie,'https://trade.kraken.com/fr-fr/charts/KRAKEN:DASH-EUR')