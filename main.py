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
import time

#CONSTANTS

MONEY=['BTC','ETH','LTC','MLN']
MONEY_SCRAPPERS=dict()

def init_scrappers (element,*args):
    MONEY_SCRAPPERS[element]=Scrapper.Scrapper(element)
    
for element in MONEY :
    Thread(target=partial(init_scrappers,element), args=(1,)).start()
    time.sleep(3)


#VARIABLES

app = tk.Tk()
app.title('VisioCrypto')
app.wm_iconbitmap('icon.ico')
global_counter = 1
df_to_plot=pd.DataFrame({'Value':[],'Date':[]})

global list_plot
global list_money_plot
list_money_plot=[]

#FONCTION


def update_plot():
    global global_counter
    global list_plot
    global list_data_plot
    global subplot
    global liste
    global MONEY_SCRAPPERS
    global list_money_plot
    
    values=[var1.get(), var2.get(), var3.get(), var4.get(), var5.get(), var6.get(), var7.get(), var8.get()]
    if (values.count("0") < 7):
        for i,money in enumerate(list_money_plot):
            try:
                list_plot[i-1].lines.pop(0)
            except:
                print("aucune ligne")
            
            list_plot[i-1].plot(MONEY_SCRAPPERS[money].dataFrame.Date,MONEY_SCRAPPERS[money].dataFrame.Value,':o',color='orange')
            fig.autofmt_xdate(rotation= 45)
            canvas.draw()
    
    elif (values.count("0") < 8):
        try:
            list_plot[0].lines.pop(0)
        except:
            print('aucune courbe à supprimer !')
        list_plot[0].plot(MONEY_SCRAPPERS[MONEY[liste[0]]].dataFrame.Date,MONEY_SCRAPPERS[MONEY[liste[0]]].dataFrame.Value,':o',color='orange')
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
    global list_money_plot
    
    values=[var1.get(), var2.get(), var3.get(), var4.get(), var5.get(), var6.get(), var7.get(), var8.get()]
    
    for i,money in enumerate(values):
        if (money == "0"):
            if i<4 and MONEY[i] in list_money_plot:
                Thread(target=MONEY_SCRAPPERS[MONEY[i]].start_and_stop, args=(1,)).start()
                print("\n",MONEY[i])
                print("\n",list_money_plot)
                list_money_plot.remove(MONEY[i])
        
        if (money != "0"):
            if MONEY[i] not in list_money_plot:
                Thread(target=MONEY_SCRAPPERS[money].start_and_stop, args=(1,)).start()  
                list_money_plot.append(MONEY[i])
        
    refresh()


global liste
liste = []

def cb():
    
    global list_plot
    global values
    global fig
    global liste
    
    for ax in fig.get_axes():
        fig.delaxes(ax)
        
    list_plot=[]
    liste=[]
    
    values=[var1.get(), var2.get(), var3.get(), var4.get(), var5.get(), var6.get(), var7.get(), var8.get()]
    
    for value in values:
        if value!="0":
            number_checked(value)
        else:
            print("box unchecked")
    
    print("----------------")
    print (liste)
    print("----------------")
    
    
    if (len(liste)==2):
        for i in range(1,3):
            list_plot.append(fig.add_subplot(1,2,i))
        print(list_plot)
        
    elif (len(liste)==1):
        list_plot.append(fig.add_subplot(1,1,1))
        print(list_plot)

    choose_money()

def number_checked(value):
    global liste
    values=[var1.get(), var2.get(), var3.get(), var4.get(), var5.get(), var6.get(), var7.get(), var8.get()]
    
    if (values.count("0") < 7):
        j = values.index(value)
        liste.append(j)
        print(value, j)
        if (len(liste)>1):
            for element in range(8):
                if element not in liste:
                    button_list[element].config(state=tk.DISABLED)
        
                
    elif (values.count("0") < 8):
        for button in button_list:
            button.config(state=tk.NORMAL)
        liste.append(values.index(value))
        print (value)
        
#---- READ THE CSV ----

fig = Figure()

frame_multi_plot=tk.Frame(app)
frame_plot=tk.Frame(frame_multi_plot)


canvas = FigureCanvasTkAgg(fig, master=frame_plot)  # A tk.DrawingArea.
canvas.get_tk_widget().pack(fill="both", expand=True)
frame_plot.pack(fill='both',side='left',expand=True)


#on crée une Frame qui va contenir les bouttons
frame_button=tk.Frame(frame_multi_plot)

var1=tk.StringVar()
var2=tk.StringVar()
var3=tk.StringVar()
var4=tk.StringVar()
var5=tk.StringVar()
var6=tk.StringVar()
var7=tk.StringVar()
var8=tk.StringVar()

#On défnit chaque boutton pour chaque monnaie avec comme paramètre le nom de la monnaie 
button_btc = tk.Checkbutton(frame_button, text='Bitcoin', variable=var1, onvalue="BTC", command=cb)
button_eth = tk.Checkbutton(frame_button, text='Ethereum', variable=var2, onvalue="ETH", command=cb)
button_ltc = tk.Checkbutton(frame_button, text='Litecoin', variable=var3, onvalue="LTC", command=cb)
button_mon = tk.Checkbutton(frame_button, text='Monero', variable=var4, onvalue="MLN", command=cb)
button_rip = tk.Checkbutton(frame_button, text='EOS', variable=var5, onvalue="EOS", command=cb)
button_car = tk.Checkbutton(frame_button, text='ATOM', variable=var6, onvalue="ATOM", command=cb)
button_das = tk.Checkbutton(frame_button, text='Dash', variable=var7, onvalue="Dash", command=cb)
button_lib = tk.Checkbutton(frame_button, text='WAVES', variable=var8, onvalue="Waves", command=cb)
button_list = [button_btc, button_eth, button_ltc, button_mon, button_rip, button_car, button_das, button_lib]

for button in button_list:
    button.deselect()
    button['indicatoron'] = 0 
    button.pack(fill='both',expand=True,side="top")


frame_button.pack(fill='y',side="right")
frame_multi_plot.pack(fill='both',expand=True)
app.mainloop()

for scrapper in MONEY:
    MONEY_SCRAPPERS[scrapper].destroy_thread()
    #MONEY_SCRAPPERS[scrapper].filling_csv()



