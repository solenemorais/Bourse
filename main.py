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
    driver = webdriver.Chrome() 
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
subplot_1 = fig.add_subplot(1,1,1) #nrows, ncols, and index in order
canvas = FigureCanvasTkAgg(fig, master=frame_plot)  # A tk.DrawingArea.
canvas.get_tk_widget().pack(fill="both", expand=True)
frame_plot.pack(fill='both',side='left',expand=True)


#on crée une Frame qui va contenir les bouttons
frame_button=tk.Frame(app)

var1=tk.StringVar()
var2=tk.StringVar()
var3=tk.StringVar()
var4=tk.StringVar()
var5=tk.StringVar()
var6=tk.StringVar()
var7=tk.StringVar()
var8=tk.StringVar()

#On défnit chaque boutton pour chaque monnaie avec comme paramètre le nom de la monnaie 
button_btc = tk.Checkbutton(frame_button, text='Bitcoin', variable=var1, onvalue=1, offvalue=0, command=partial(choose_money, "BTC"))
button_eth = tk.Checkbutton(frame_button, text='Ethereum', variable=var2, onvalue="ETH", offvalue=0)
button_ltc = tk.Checkbutton(frame_button, text='Litecoin', variable=var3, onvalue="LTC", offvalue=0)
button_mon = tk.Checkbutton(frame_button, text='Monero', variable=var4, onvalue="MNL", offvalue=0)
button_rip = tk.Checkbutton(frame_button, text='EOS', variable=var5, onvalue="EOS", offvalue=0)
button_car = tk.Checkbutton(frame_button, text='ATOM', variable=var6, onvalue="ATOM", offvalue=0)
button_das = tk.Checkbutton(frame_button, text='Dash', variable=var7, onvalue="Dash", offvalue=0)
button_lib = tk.Checkbutton(frame_button, text='WAVES', variable=var8, onvalue="Waves", offvalue=0)

button_btc.deselect()
#button_btc['indicatoron'] = 0 
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

    


