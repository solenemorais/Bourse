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
from threading import Thread
import pandas as pd
from datetime import datetime

#Variables
app = tk.Tk()
app.title('VisioCrypto')
app.wm_iconbitmap('icon.ico')

global GLOBAL_COUNTER
GLOBAL_COUNTER = 1


#ici en fonction de la monnaie choisie on va exécuter la fonction correspondante

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
df=pd.DataFrame({'Value':[],'Date':[]})

#Ici on a les différentes fonctions qui font être exécutées en fonction de la monnaie choisis
def scrap(name,driver,*args):
    while True :
        price=driver.find_element_by_id("price-ticker").find_elements_by_tag_name('span')[1]
        print(price.text)
        df.loc[df.shape[0]]=[float(price.text[:-4]),datetime.now()]
        #filling_csv(name,df)
        time.sleep(PAUSE)
    
def get_data_csv(name):
    filename=str(name+'.csv')
    file_exists = os.path.isfile(filename)
    if file_exists :
        df=pd.read_csv(filename,sep="/")

def filling_csv (name,df):
    filename=str(name+'.csv')
    file_exists = os.path.isfile(filename)
    if file_exists :
        with open(filename, 'a+', newline="") as csv_file:
            fieldnames = ["Value", "Date"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter="/")
            for row in df.itertuples() :
                writer.writerow({"Value" : row.data, "Date" : row.time})
    else:
        #---- CREATE A NEW CSV ----
        with open(filename, 'w', newline="") as csv_file:
            fieldnames = ["Value", "Date"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter="/")
            writer.writeheader()
            for row in df.itertuples() :
                writer.writerow({"Value" : row.data, "Date" : row.time})
           
def update_plot():
    global GLOBAL_COUNTER
    fig.delaxes(fig.get_axes()[0])
    subplot_1 = fig.add_subplot(1,1,1)
    subplot_1.plot(df.Date,df.Value)
    fig.autofmt_xdate(rotation= 45)
    canvas.draw()


def refresh():
    global GLOBAL_COUNTER
    app.after(500, refresh)
    update_plot()
    GLOBAL_COUNTER+=1
            
            
            
#ici en fonction de la monnaie choisie on va exécuter la fonction correspondante
#Par exemple ici si la monnaie est BTC on va exécuter la fonction BTC()    

    
def choose_money(money):
    driver=webdriver.Firefox()
    
    if money=="BTC":
        driver.get('https://trade.kraken.com/fr-fr/charts/KRAKEN:BTC-EUR')
        get_data_csv(money)
        
        thread_2 = Thread(target=refresh(), args=(1,))
        thread_1 = Thread(target=partial(scrap,money,driver), args=(1,))
        thread_1.start()
        time.sleep(5)
        thread_2.start()
        
        
    elif money=="ETH":
        driver.get('https://trade.kraken.com/fr-fr/charts/KRAKEN:ETH-EUR')
        get_data_csv(money)
        
        thread_2 = Thread(target=refresh(), args=(1,))
        thread_1 = Thread(target=partial(scrap,money,driver), args=(1,))
        thread_1.start()
        time.sleep(5)
        thread_2.start()
        
    elif money=="LTC":
        driver.get('https://trade.kraken.com/fr-fr/charts/KRAKEN:LTC-EUR')
        get_data_csv(money)
        
        thread_2 = Thread(target=refresh(), args=(1,))
        thread_1 = Thread(target=partial(scrap,money,driver), args=(1,))
        thread_1.start()
        time.sleep(5)
        thread_2.start()
        
    elif money=="MON":
        driver.get('https://trade.kraken.com/fr-fr/charts/KRAKEN:MLN-EUR')
        get_data_csv(money)
        
        thread_2 = Thread(target=refresh(), args=(1,))
        thread_1 = Thread(target=partial(scrap,money,driver), args=(1,))
        thread_1.start()
        time.sleep(5)
        thread_2.start()
        
    elif money=="EOS":
        driver.get('https://trade.kraken.com/fr-fr/charts/KRAKEN:EOS-EUR')
        get_data_csv(money)
        
        thread_2 = Thread(target=refresh(), args=(1,))
        thread_1 = Thread(target=partial(scrap,money,driver), args=(1,))
        thread_1.start()
        time.sleep(5)
        thread_2.start()
        
    elif money=="CAR":
        driver.get('https://trade.kraken.com/fr-fr/charts/KRAKEN:ATOM-EUR')
        get_data_csv(money)
        
        thread_2 = Thread(target=refresh(), args=(1,))
        thread_1 = Thread(target=partial(scrap,money,driver), args=(1,))
        thread_1.start()
        time.sleep(5)
        thread_2.start()
        
    elif money=="WAVE":
        driver.get('https://trade.kraken.com/fr-fr/charts/KRAKEN:WAVES-EUR')
        get_data_csv(money)
        
        thread_2 = Thread(target=refresh(), args=(1,))
        thread_1 = Thread(target=partial(scrap,money,driver), args=(1,))
        thread_1.start()
        time.sleep(5)
        thread_2.start()
        
    elif money=="DASH":
        driver.get('https://trade.kraken.com/fr-fr/charts/KRAKEN:DASH-EUR')
        get_data_csv(money)
        
        thread_2 = Thread(target=refresh(), args=(1,))
        thread_1 = Thread(target=partial(scrap,money,driver), args=(1,))
        thread_1.start()
        time.sleep(5)
        thread_2.start()


#---- READ THE CSV ----
"""
PATH_FILE_NAME = "scrape_data.csv"

df = pd.read_csv(PATH_FILE_NAME, sep=";")

df["Date"] = df["Date"].astype(str)
df["Date"] = df["Date"].apply(lambda x: datetime.fromisoformat(x))

df = df.sort_values('Date')
df = df.reset_index(drop=True)

column_list = list(df.columns)
column_list.remove('Date')
"""
fig = Figure()
frame_plot=tk.Frame(app)
subplot_1 = fig.add_subplot(1,1,1)
canvas = FigureCanvasTkAgg(fig, master=frame_plot)  # A tk.DrawingArea.
canvas.get_tk_widget().pack(fill="both", expand=True)
frame_plot.pack(fill='both',side='left',expand=True)

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
button_btc.pack(fill='both',expand=True,side="top")
button_eth.pack(fill='both',expand=True,side="top")
button_ltc.pack(fill='both',expand=True,side="top")
button_mon.pack(fill='both',expand=True,side="top")
button_rip.pack(fill='both',expand=True,side="top")
button_car.pack(fill='both',expand=True,side="top")
button_das.pack(fill='both',expand=True,side="top")
button_lib.pack(fill='both',expand=True,side="top")

#on place la frame dans l'appli en haut de celle ci
frame_button.pack(fill='y',side="right")
app.mainloop()

    


