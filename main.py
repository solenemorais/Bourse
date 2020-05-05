# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 17:27:00 2020

@author: Aurélien
"""

#Ce fichier sera le main du coup faudra pas changer le nom dans le différentes branche pour qu'on puisse les fusionner après
#Import
import tkinter as tk
from functools import partial
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import pandas as pd
from datetime import datetime

#Variables
app = tk.Tk()
app.title('VisioCrypto')

global GLOBAL_COUNTER
GLOBAL_COUNTER = 1


#ici en fonction de la monnaie choisie on va exécuter la fonction correspondante

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
    
def choose_money(money):
    if money=="BTC":
        get_BTC()
    elif money=="ETH":
        get_ETH()
    elif money=="LTC":
        get_LTC()
    elif money=="MON":
        get_MON()
    elif money=="RIP":
        get_RIP()
    elif money=="CAR":
        get_CAR()
    elif money=="DAS":
        get_DAS()
    elif money=="LIB":
        get_LIB()

def lauch():
    #---- READ THE CSV ----
    PATH_FILE_NAME = "scrape_data.csv"
    
    df = pd.read_csv(PATH_FILE_NAME, sep=";")
    print(df.dtypes)
    
    df["Date"] = df["Date"].astype(str)
    df["Date"] = df["Date"].apply(lambda x: datetime.fromisoformat(x))
    print(df.dtypes)
    
    df = df.sort_values('Date')
    df = df.reset_index(drop=True)
    
    column_list = list(df.columns)
    column_list.remove('Date')

    label = tk.Label(text="")
    label.pack()
    
    fig = Figure()
    
    subplot_1 = fig.add_subplot(1,1,1)
    canvas = FigureCanvasTkAgg(fig, master=app)  # A tk.DrawingArea.
    canvas.get_tk_widget().pack(fill="both", expand=1)
    #on crée une Frame qui va contenir les bouttons
    
    def update_plot():
        global GLOBAL_COUNTER
        print(fig.get_axes())
        fig.delaxes(fig.get_axes()[0])
        print(fig.get_axes())
        subplot_1 = fig.add_subplot(1,1,1)
        date_list = df['Date'][:GLOBAL_COUNTER].to_list()

        for column in column_list:
            value_list = df[column][:GLOBAL_COUNTER].to_list()
            line = subplot_1.plot_date([date_list],[value_list])
        canvas.draw()


    def refresh():
        global GLOBAL_COUNTER
        print("refresh")
        app.after(500, refresh)
        update_plot()
        GLOBAL_COUNTER+=1
    
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
    refresh()
    app.mainloop()
    


lauch()


