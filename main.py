# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 17:27:00 2020

@author: Aurélien
"""

#Ce fichier sera le main du coup faudra pas changer le nom dans le différentes branche pour qu'on puisse les fusionner après

#Ici on a les différentes fonctions qui font être exécutées en fonction de la monnaie choisis
def BTC():#BITCOIN
    print("BTC")

def ETH():#Ethereum
    print("ETH")
    
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
monnaie="BTC"

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