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
import Scrapper
from threading import Thread
import pandas as pd
from functools import partial

#CONSTANTS

MONEY=['BTC','ETH','LTC','MLN','EOS','ATOM','Dash','Waves']
MONEY_SCRAPPERS=dict()
"""
for element in MONEY :
    MONEY_SCRAPPERS[element]=Scrapper.Scrapper(element)
"""

MONEY_SCRAPPERS["BTC"]=Scrapper.Scrapper("BTC")
MONEY_SCRAPPERS["ETH"]=Scrapper.Scrapper("ETH")
#VARIABLES
global list_test
list_test=[]


app = tk.Tk()
app.title('VisioCrypto')
app.wm_iconbitmap('icon.ico')
global_counter = 1
df_to_plot=pd.DataFrame({'Value':[],'Date':[]})


#FONCTION


def update_plot():
    global global_counter
    global df_to_plot
    global list_test
    global list_data_plot
    
    for index in range(len(fig.get_axes())-1):
        fig.delaxes(fig.get_axes()[index])
    
    for i,data in enumerate(list_data_plot):
        subplot = fig.add_subplot(2,2,i+1)
        subplot.plot(data.Date,data.Value,color='orange')
        fig.autofmt_xdate(rotation= 45)
        canvas.draw()
    
def refresh():
    global global_counter
    global list_test
    update_plot()
    global_counter+=1
    app.after(500, refresh)
            
            
            
#ici en fonction de la monnaie choisie on va exécuter la fonction correspondante
#Par exemple ici si la monnaie est BTC on va exécuter la fonction BTC()    
    
 
def choose_money():
    global df_to_plot
    global list_data_plot
    global list_test
    for money in list_test:
        print(money)
        Thread(target=MONEY_SCRAPPERS[money].start_and_stop, args=(1,)).start()
        list_data_plot.append(MONEY_SCRAPPERS[money].dataFrame)
    refresh()

global list_data_plot
list_data_plot = []

def mget():
    global list_test
    values=[var1.get(), var2.get(), var3.get(), var4.get(), var5.get(), var6.get(), var7.get(), var8.get()]
    for value in values:
        if (value != "0"):
            list_test.append(value)
    choose_money()
        

#---- READ THE CSV ----

fig = Figure()
frame_plot=tk.Frame(app)
subplot = fig.add_subplot(1,1,1)
    
"""  
subplot_1 = fig.add_subplot(2,2,1) #nrows, ncols, and index in order
subplot_2 = fig.add_subplot(2,2,2)
subplot_3 = fig.add_subplot(2,2,3)
subplot_4 = fig.add_subplot(2,2,4)
"""
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
button_btc = tk.Checkbutton(frame_button, text='Bitcoin', variable=var1, onvalue="BTC")
button_eth = tk.Checkbutton(frame_button, text='Ethereum', variable=var2, onvalue="ETH")
button_ltc = tk.Checkbutton(frame_button, text='Litecoin', variable=var3, onvalue="LTC")
button_mon = tk.Checkbutton(frame_button, text='Monero', variable=var4, onvalue="MLN")
button_rip = tk.Checkbutton(frame_button, text='EOS', variable=var5, onvalue="EOS")
button_car = tk.Checkbutton(frame_button, text='ATOM', variable=var6, onvalue="ATOM")
button_das = tk.Checkbutton(frame_button, text='Dash', variable=var7, onvalue="Dash")
button_lib = tk.Checkbutton(frame_button, text='WAVES', variable=var8, onvalue="Waves")


button_list = [button_btc, button_eth, button_ltc, button_mon, button_rip, button_car, button_das, button_lib]

for button in button_list:
    button.deselect()
    #button['indicatoron'] = 0 
    button.pack(fill='both',expand=True,side="top")
    


button_plot = tk.Button(frame_button, text="PLOT", command=mget)
button_plot.pack()
    
#button_btc['indicatoron'] = 0 
#on place chaque boutton dans l'appli avec comme paramètre side=left pour qu'il soit tous au milieu de l'appli
#on place la frame dans l'appli en haut de celle ci


frame_button.pack(fill='y',side="right")
app.mainloop()

for scrapper in MONEY:
    MONEY_SCRAPPERS[scrapper].destroy_thread()
    MONEY_SCRAPPERS[scrapper].filling_csv()



