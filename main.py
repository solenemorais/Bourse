# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 17:27:00 2020

@author: Aurélien
"""

#Ce fichier sera le main du coup faudra pas changer le nom dans le différentes branche pour qu'on puisse les fusionner après

#Ici on a les différentes fonctions qui font être exécutées en fonction de la monnaie choisis
def get_BTC():#BITCOIN
    print("BTC")

def get_ETH():#Ethereum
    print("ETH")
    
def get_LTC():#Litecoin
    print("LTC")

def get_MON():#Monero
    print("MON")

def get_RIP():#Ripple
    print("RIP")

def get_CAR():#Cardano
    print("CAR")
    
def get_DAS():#Dash
    print("DAS")
    
def get_LIB():#Libra
    print("LIB")

#ici en fonction de la monnaie choisie on va exécuter la fonction correspondante
#Par exemple ici si la monnaie est BTC on va exécuter la fonction BTC()    
monnaie="BTC"

if monnaie=="BTC":
    get_BTC()
elif monnaie=="ETH":
    get_ETH()
elif monnaie=="LTC":
    get_LTC()
elif monnaie=="MON":
    get_MON()
elif monnaie=="RIP":
    get_RIP()
elif monnaie=="CAR":
    get_CAR()
elif monnaie=="DAS":
    get_DAS()
elif monnaie=="LIB":
    get_LIB()