# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 17:27:00 2020

@author: Aurélien
"""

#Ce fichier sera le main du coup faudra pas changer le nom dans le différentes branche pour qu'on puisse les fusionner après

#IMPORT
import time
from selenium import webdriver
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#CONSTANTE
PAUSE=10

#VARIABLE
dataFrame=pd.DataFrame({'data':[],'time':[]})

#Ici on a les différentes fonctions qui font être exécutées en fonction de la monnaie choisis
def BTC():#BITCOIN
    print("BTC")

def ETH():#Ethereum
    print("ETH")
    driver=webdriver.Firefox()
    driver.get('https://trade.kraken.com/fr-fr/charts/KRAKEN:ETH-EUR')
    while(True):
        price=driver.find_element_by_id("price-ticker").find_elements_by_tag_name('span')[1]
        localTime=time.localtime();
        data_time=str(localTime.tm_hour)+":"+str(localTime.tm_min)+":"+str(localTime.tm_sec)
        dataFrame.loc[dataFrame.shape[0]]=[float(price.text[:-4]),data_time]
        print(dataFrame)
        dataFrame.to_excel("ETH.xlsx")
        time.sleep(PAUSE)
        
def LTC():#Litecoin
    print("LTC")

def MON():#Monero
    print("MON")

def RIP():#Ripple
    print("RIP")

def CAR():#Cardano
    print("CAR")
    
def DAS():#Dash
    print("DAS")
    
def LIB():#Libra
    print("LIB")

#ici en fonction de la monnaie choisie on va exécuter la fonction correspondante
#Par exemple ici si la monnaie est BTC on va exécuter la fonction BTC()    
monnaie="ETH"
if monnaie=="BTC":
    BTC()
elif monnaie=="ETH":
    ETH()
elif monnaie=="LTC":
    LTC()
elif monnaie=="MON":
    MON()
elif monnaie=="RIP":
    RIP()
elif monnaie=="CAR":
    CAR()
elif monnaie=="DAS":
    DAS()
elif monnaie=="LIB":
    LIB()