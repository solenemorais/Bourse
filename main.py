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
import time
import tkinter as tk
import tkinter.font as tkFont

compte=1000
investement=0
invest_money=""
flag_invest=False

#CONSTANTS

MONEY=['BTC','ETH','LTC']#,'MLN','EOS','ATOM','DASH','WAVES']
MONEY_SCRAPPERS=dict()

def init_scrappers(element,*args):
    MONEY_SCRAPPERS[element]=Scrapper.Scrapper(element)
    
for element in MONEY :
    Thread(target=partial(init_scrappers,element), args=(1,)).start()   
    time.sleep(1)

#VARIABLES
app = tk.Tk()
app.title('VisioCrypto')
app.wm_iconbitmap('icon.ico')
global_counter = 1
df_to_plot=pd.DataFrame({'Value':[],'Date':[]})


#FONCTION
     
def update_plot():
    global global_counter
    global df_to_plot
    fig.delaxes(fig.get_axes()[0])
    subplot_1 = fig.add_subplot(1,1,1)
    if df_to_plot.shape[0] > 3:
        subplot_1.plot(df_to_plot['Date'][:-1],df_to_plot['Value'][:-1],":o",color="orange")
        subplot_1.plot(df_to_plot['Date'][-2:],df_to_plot['Value'][-2:],"--",color="purple")
        fig.autofmt_xdate(rotation= 45)
        canvas.draw()
    else:
        subplot_1.plot(df_to_plot['Date'],df_to_plot['Value'],":o",color="orange")
        fig.autofmt_xdate(rotation= 45)
        canvas.draw()

def refresh():
    global global_counter
    update_plot()
    global_counter+=1
    app.after(500, refresh)
                 
            
#ici en fonction de la monnaie choisie on va exécuter la fonction correspondante
#Par exemple ici si la monnaie est BTC on va exécuter la fonction BTC()    


def invest (flag,*args):
    global var_compte
    global var_invest
    global compte
    global investement
    global invest_money
    global MONEY_SCRAPPERS
    global Entry_text
    global var_invest
    global var_compte
    
    if invest_money != "" :
        if flag==True and MONEY_SCRAPPERS[invest_money].thread_flag_invest == False :
            print(Entry_text.get())
            if Entry_text.get()!='':
                print(1)
                compte=compte-int(Entry_text.get())
                investement=investement+int(Entry_text.get())
            MONEY_SCRAPPERS[invest_money].thread_flag_invest=flag
            Thread(target=partial(MONEY_SCRAPPERS[invest_money].start_and_stop_invest,compte,investement), args=(1,)).start()
            Thread(target=plot, args=(1,)).start()
            
        elif flag==True and MONEY_SCRAPPERS[invest_money].thread_flag_invest == True:
            MONEY_SCRAPPERS[invest_money].invest=MONEY_SCRAPPERS[invest_money].invest+int(Entry_text.get())
            MONEY_SCRAPPERS[invest_money].compte=MONEY_SCRAPPERS[invest_money].compte-int(Entry_text.get())
            
            
        if flag==False:
            MONEY_SCRAPPERS[invest_money].thread_flag_invest=flag
            print(MONEY_SCRAPPERS[invest_money].dataFrame['Value'][MONEY_SCRAPPERS[invest_money].dataFrame.shape[0]-1])
            compte=(MONEY_SCRAPPERS[invest_money].invest*MONEY_SCRAPPERS[invest_money].dataFrame['Value'][MONEY_SCRAPPERS[invest_money].dataFrame.shape[0]-1])+MONEY_SCRAPPERS[invest_money].compte
            MONEY_SCRAPPERS[invest_money].compte=compte
            
            investement=0 
            MONEY_SCRAPPERS[invest_money].invest=investement
            
    else :
        tk.messagebox.showinfo("Attention", "Vous devez choisir une monnaie")
        
        
def plot(*args):
    global invest_money
    global compte
    global investement
    global MONEY_SCRAPPERS
    global var_invest
    global var_compte
    
    while MONEY_SCRAPPERS[invest_money].thread_flag_invest == True :
        var_invest.set(str(MONEY_SCRAPPERS[invest_money].invest))
        investement=MONEY_SCRAPPERS[invest_money].invest
        var_compte.set(str(MONEY_SCRAPPERS[invest_money].compte))
        compte=MONEY_SCRAPPERS[invest_money].compte
        
    var_invest.set(str(investement))
    var_compte.set(str(compte))
        
def choose_money(money):
    global df_to_plot
    global invest_money
    invest_money=money
    Thread(target=MONEY_SCRAPPERS[money].start_and_stop_scrap, args=(1,)).start() 
    df_to_plot=MONEY_SCRAPPERS[money].dataFrame
    refresh()
    
#---- READ THE CSV ----

frame_plot_button=tk.Frame(app)

fig = Figure()
frame_plot=tk.Frame(frame_plot_button)
subplot_1 = fig.add_subplot(1,1,1) #nrows, ncols, and index in order
canvas = FigureCanvasTkAgg(fig, master=frame_plot)  # A tk.DrawingArea.
canvas.get_tk_widget().pack(fill="both", expand=True)
frame_plot.pack(fill='both',side='left', expand=True)


#on crée une Frame qui va contenir les bouttons

frame_button=tk.Frame(frame_plot_button)
frame_my_money=tk.Frame(app)
var1=tk.StringVar()
var2=tk.StringVar()
var3=tk.StringVar()
var4=tk.StringVar()
var5=tk.StringVar()
var6=tk.StringVar()
var7=tk.StringVar()
var8=tk.StringVar()

#On défnit chaque boutton pour chaque monnaie avec comme paramètre le nom de la monnaie 
button_btc = tk.Checkbutton(frame_button, text='Bitcoin', variable=var1, onvalue=1, offvalue=0, command=partial(choose_money, MONEY[0]))
button_eth = tk.Checkbutton(frame_button, text='Ethereum', variable=var2, onvalue=1, offvalue=0, command=partial(choose_money, MONEY[1]))
button_ltc = tk.Checkbutton(frame_button, text='Litecoin', variable=var3, onvalue=1, offvalue=0, command=partial(choose_money, MONEY[2]))
"""
button_mon = tk.Checkbutton(frame_button, text='Monero', variable=var4, onvalue=1, offvalue=0, command=partial(choose_money, MONEY[3]))
button_rip = tk.Checkbutton(frame_button, text='EOS', variable=var5, onvalue=1, offvalue=0, command=partial(choose_money, MONEY[4]))
button_car = tk.Checkbutton(frame_button, text='ATOM', variable=var6, onvalue=1, offvalue=0, command=partial(choose_money, MONEY[5]))
button_das = tk.Checkbutton(frame_button, text='Dash', variable=var7, onvalue=1, offvalue=0, command=partial(choose_money, MONEY[6]))
button_lib = tk.Checkbutton(frame_button, text='WAVES', variable=var8, onvalue=1, offvalue=0, command=partial(choose_money, MONEY[7]))
"""
button_btc.deselect()
button_eth.deselect()
button_ltc.deselect()
"""
button_mon.deselect()
button_rip.deselect()
button_car.deselect()
button_das.deselect()
button_lib.deselect()
"""
#button_btc['indicatoron'] = 0 
#on place chaque boutton dans l'appli avec comme paramètre side=left pour qu'il soit tous au milieu de l'appli
button_btc.pack(fill='both',expand=True,side="top")
button_eth.pack(fill='both',expand=True,side="top")
button_ltc.pack(fill='both',expand=True,side="top")
"""
button_mon.pack(fill='both',expand=True,side="top")
button_rip.pack(fill='both',expand=True,side="top")
button_car.pack(fill='both',expand=True,side="top")
button_das.pack(fill='both',expand=True,side="top")
button_lib.pack(fill='both',expand=True,side="top")
"""
#on place la frame dans l'appli en haut de celle ci

var_compte = tk.StringVar()
var_compte.set(str(compte))

var_invest = tk.StringVar()
var_invest.set(str(investement))

label_my_money=tk.Label(frame_my_money,text='Compte :',pady=10,padx=10)
label_money=tk.Label(frame_my_money,textvariable =var_compte,pady=10)

label_my_money.pack(side='left')
label_money.pack(side='left')

label_my_money=tk.Label(frame_my_money,text='Unity :',pady=10,padx=10)
label_money=tk.Label(frame_my_money,textvariable=var_invest,pady=10)

label_my_money.pack(side='left')
label_money.pack(side='left')

button_stop_invest = tk.Button(frame_my_money, text='Stop',command=partial(invest,False),padx=10)
button_stop_invest.pack( side = 'right')

button_invest = tk.Button(frame_my_money, text='Go',command=partial(invest,True),padx=10)
button_invest.pack( side = 'right')

Entry_text = tk.StringVar()
Entry_text.set('')
Entry_money_invest = tk.Entry(frame_my_money,textvariable=Entry_text)
Entry_money_invest.pack(side = 'right')

Label_money_invest = tk.Label(frame_my_money, text="Invest :",padx=10, pady=10)
Label_money_invest.pack( side = 'right')


frame_my_money.pack(fill='x',side="top")
frame_button.pack(fill='y',side="right")
frame_plot_button.pack(fill='both',side="top",expand=True)

app.mainloop()

for scrapper in MONEY:
    Thread(target=MONEY_SCRAPPERS[scrapper].destroy(), args=(1,)).start()
    



