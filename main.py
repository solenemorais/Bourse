# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 17:27:00 2020

@author: Aurélien
"""

#IMPORT

import tkinter as tk
from functools import partial
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from threading import Thread
import pandas as pd
from datetime import datetime
import csv
import os.path
import time
from selenium import webdriver

#CONSTANTE

PAUSE=10

#VARIABLES

app = tk.Tk()
app.title('VisioCrypto')
app.wm_iconbitmap('icon.ico')
df=pd.DataFrame({'Value':[],'Date':[]})
global_counter = 1


#FONCTION

#Fonction qui va scrapper la donnée et la stocker dans la dataFrame et le csv
def scrap(name,*args):
    global df
    driver=webdriver.Firefox()
    url=str('https://trade.kraken.com/fr-fr/charts/KRAKEN:'+name+'-EUR')
    driver.get(url)
    
    while True :
        price=driver.find_element_by_id("price-ticker").find_elements_by_tag_name('span')[1]
        print(price.text)
        df.loc[df.shape[0]]=[float(price.text[:-4]),datetime.now()]
        filling_csv(name)
        time.sleep(PAUSE)

#Fonction qui va checker si un csv de la donnée scrapper existe et si oui remplir la dataFrame avec
def get_data_csv(name):
    global df
    filename=str(name+'.csv')
    file_exists = os.path.isfile(filename)
    print(df)
    if file_exists :
        df=pd.read_csv(filename,sep="/").reset_index(drop=True)
        print (df)
        df["Date"] = df["Date"].astype(str)
        df["Date"] = df["Date"].apply(lambda x: datetime.fromisoformat(x))
        print(df)

#Fonction qui va remplir le csv avec la dataFrame 
def filling_csv (name):
    global df
    filename=str(name+'.csv')
    file_exists = os.path.isfile(filename)
    if file_exists :
        #os.remove(filename)
        with open(filename, 'w', newline="") as csv_file:
            fieldnames = ["Value", "Date"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter="/")
            writer.writeheader()
            for row in df.itertuples() :
                writer.writerow({"Value" : row.Value, "Date" : row.Date})
    else:
        #---- CREATE A NEW CSV ----
        with open(filename, 'w', newline="") as csv_file:
            fieldnames = ["Value", "Date"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter="/")
            writer.writeheader()
            for row in df.itertuples() :
                writer.writerow({"Value" : row.Value, "Date" : row.Date})
           
def update_plot():
    global global_counter
    global df
    fig.delaxes(fig.get_axes()[0])
    subplot_1 = fig.add_subplot(1,1,1)
    subplot_1.plot(df.Date,df.Value,color='orange')
    fig.autofmt_xdate(rotation= 45)
    canvas.draw()


def refresh():
    global global_counter
    update_plot()
    global_counter+=1
    app.after(500, refresh)
            
            
            
#ici en fonction de la monnaie choisie on va exécuter la fonction correspondante
#Par exemple ici si la monnaie est BTC on va exécuter la fonction BTC()    
    
def choose_money(money):
    get_data_csv(money)
    refresh()
    thread_scrap = Thread(target=partial(scrap,money), args=(1,))
    thread_scrap.start()
    
    
#---- READ THE CSV ----

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
button_mon = tk.Button(frame_button,text="Monero",command=partial(choose_money,"MLN"))
button_rip = tk.Button(frame_button,text="EOS",command=partial(choose_money,"EOS"))
button_car = tk.Button(frame_button,text="ATOM",command=partial(choose_money,"ATOM"))
button_das = tk.Button(frame_button,text="Dash",command=partial(choose_money,"DASH"))
button_lib = tk.Button(frame_button,text="WAVES",command=partial(choose_money,"WAVES"))

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

    


