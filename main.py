# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 17:27:00 2020

@author: Aurélien
"""

#Ce fichier sera le main du coup faudra pas changer le nom dans le différentes branche pour qu'on puisse les fusionner après
#Import
import tkinter as tk
from functools import partial

#Variables
app = tk.Tk()
app.title('My App')

#ici en fonction de la monnaie choisie on va exécuter la fonction correspondante

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

def choose_money(money):
    if money=="BTC":
        BTC()
    elif money=="ETH":
        ETH()
    elif money=="LTC":
        LTC()
    elif money=="MON":
        MON()
    elif money=="RIP":
        RIP()
    elif money=="CAR":
        CAR()
    elif money=="DAS":
        DAS()
    elif money=="LIB":
        LIB()

def lauch():
    #on crée une Frame qui va contenir les bouttons
    frame_button=tk.Frame(app)
    
    #On défnit chaque boutton pour chaque monnaie avec comme paramètre le nom de la monnaie 
    button_btc = tk.Button(frame_button,text="Bitcoin",command=partial(choose_money,"BTC"))
    button_eth = tk.Button(frame_button,text="Ethereum",command=partial(choose_money,"ETH"))
    button_ltc = tk.Button(frame_button,text="Litecoin",command=partial(choose_money,"LTC"))
    button_mon = tk.Button(frame_button,text="Monero",command=partial(choose_money,"MON"))
    button_rip = tk.Button(frame_button,text="Ripple",command=partial(choose_money,"RIP"))
    button_car = tk.Button(frame_button,text="Cardano",command=partial(choose_money,"CAR"))
    button_das = tk.Button(frame_button,text="Dash",command=partial(choose_money,"DAS"))
    button_lib = tk.Button(frame_button,text="Libra",command=partial(choose_money,"LIB"))
    
    #on place chaque boutton dans l'appli avec comme paramètre side=left pour qu'il soit tous au milieu de l'appli
    button_btc.pack(fill='x',expand=True,side="left")
    button_eth.pack(fill='x',expand=True,side="left")
    button_ltc.pack(fill='x',expand=True,side="left")
    button_mon.pack(fill='x',expand=True,side="left")
    button_rip.pack(fill='x',expand=True,side="left")
    button_car.pack(fill='x',expand=True,side="left")
    button_das.pack(fill='x',expand=True,side="left")
    button_lib.pack(fill='x',expand=True,side="left")
    
    #on place la frame dans l'appli en haut de celle ci
    frame_button.pack(fill='x',side="top")
    app.mainloop()
    

lauch()

