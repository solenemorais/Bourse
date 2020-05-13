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
import tkinter.font as tkFont

#CONSTANTS

MONEY=['BTC','ETH','LTC','MLN','EOS','ATOM','DASH','WAVES']
MONEY_SCRAPPERS=dict()

def init_scrappers (element,*args):
    MONEY_SCRAPPERS[element]=Scrapper.Scrapper(element)
    
for element in MONEY :
    Thread(target=partial(init_scrappers,element), args=(1,)).start()
    time.sleep(4)

#VARIABLES
global MODE
MODE=0

    #BACK
compte=1000 #our money
investement=0 #money we invest in a crypotmoney
invest_money="" #cryptomoney choosen for investement
stock=0
flag_invest=False #flag we wil control the invest thread

    #FRONT
global subplot_to_display #list will contain subplot of the figure
global list_money_plot #list will contain title of money displayed
global button_check_index #list will index of button clicked

subplot_to_display=[]
button_check_index = []
list_money_plot=[]

#FONCTION

def update_plot():
    
    global MODE
    global invest_money
    global subplot_to_display
    global list_data_plot
    global button_check_index
    global MONEY_SCRAPPERS
    global list_money_plot
    
    if(MODE==1):
        dataframe_money=MONEY_SCRAPPERS[invest_money].dataFrame
        
        if len(subplot_to_display[0].lines)>0 and len(subplot_to_display[0].lines)<2:
            subplot_to_display[0].lines.pop(0)
            
        elif len(subplot_to_display[0].lines)>0 and len(subplot_to_display[0].lines)>=2:
            
            subplot_to_display[0].lines.pop(0)
            subplot_to_display[0].lines.pop(0)
            
        if dataframe_money.shape[0] > 3:
            subplot_to_display[0].plot(dataframe_money['Date'][:-1],dataframe_money['Value'][:-1],":o",color="orange")
            subplot_to_display[0].plot(dataframe_money['Date'][-2:],dataframe_money['Value'][-2:],"--",color="purple")
            fig_invest.autofmt_xdate(rotation=45)
            canvas_invest.draw()
            
        else:
            subplot_to_display[0].plot(dataframe_money['Date'],dataframe_money['Value'],":o",color="orange")
            fig_invest.autofmt_xdate(rotation=45)
            canvas_invest.draw()
        
    elif(MODE==2):
        checkbox_value=[var1.get(), var2.get(), var3.get(), var4.get(), var5.get(), var6.get(), var7.get(), var8.get()]
        
        if (checkbox_value.count("0") < 7):
            for i,money in enumerate(list_money_plot):
                if len(subplot_to_display[i-1].lines)>0:
                    subplot_to_display[i-1].lines.pop(0)
                dataframe_money=MONEY_SCRAPPERS[money].dataFrame
                subplot_to_display[i-1].plot(dataframe_money.Date,dataframe_money.Value,':o',color='orange')
                fig_compare_plot.autofmt_xdate(rotation= 45)
                canvas.draw()
        
        elif (checkbox_value.count("0") < 8):
            if len(subplot_to_display[0].lines)>0:
                subplot_to_display[0].lines.pop(0)
            dataframe_money=MONEY_SCRAPPERS[MONEY[button_check_index[0]]].dataFrame
            subplot_to_display[0].plot(dataframe_money.Date,dataframe_money.Value,':o',color='orange')
            fig_compare_plot.autofmt_xdate(rotation= 45)
            canvas.draw()

def refresh():
    update_plot()
    app.after(500, refresh)
          

def start_stop_scrap_multiplot():
    
    global list_money_plot
    global checkbox_value
    
    checkbox_value=[var1.get(), var2.get(), var3.get(), var4.get(), var5.get(), var6.get(), var7.get(), var8.get()]
    
    for i,money in enumerate(checkbox_value):
        if (money == "0"):
            if MONEY[i] in list_money_plot:
                Thread(target=MONEY_SCRAPPERS[MONEY[i]].start_and_stop_scrap, args=(1,)).start()
                list_money_plot.remove(MONEY[i])
        
        if (money != "0"):
            if MONEY[i] not in list_money_plot:
                Thread(target=MONEY_SCRAPPERS[money].start_and_stop_scrap, args=(1,)).start()  
                list_money_plot.append(MONEY[i])
    refresh()



def get_checked_button():
    
    global subplot_to_display
    global fig_compare_plot
    global button_check_index
    
    for ax in fig_compare_plot.get_axes():
        fig_compare_plot.delaxes(ax)
        
    subplot_to_display=[]
    button_check_index=[]
    
    checkbox_value=[var1.get(), var2.get(), var3.get(), var4.get(), var5.get(), var6.get(), var7.get(), var8.get()]
    
    for value in checkbox_value:
        if value!="0":
            number_checked(value)   
    
    if (len(button_check_index)==2):
        for i in range(1,3):
            subplot_to_display.append(fig_compare_plot.add_subplot(1,2,i))
        
    elif (len(button_check_index)==1):
        subplot_to_display.append(fig_compare_plot.add_subplot(1,1,1))

    start_stop_scrap_multiplot()

def number_checked(value):
    global button_check_index
    
    checkbox_value=[var1.get(), var2.get(), var3.get(), var4.get(), var5.get(), var6.get(), var7.get(), var8.get()]
    
    if (checkbox_value.count("0") < 7):
        j = checkbox_value.index(value)
        button_check_index.append(j)
        if (len(button_check_index)>1):
            for element in range(8):
                if element not in button_check_index:
                    button_list[element].config(state=tk.DISABLED)
                
    elif (checkbox_value.count("0") < 8):
        for button in button_list:
            button.config(state=tk.NORMAL)
        button_check_index.append(checkbox_value.index(value))
        
                 
            
#ici en fonction de la monnaie choisie on va exécuter la fonction correspondante
#Par exemple ici si la monnaie est BTC on va exécuter la fonction BTC()    


def invest (flag,*args):

    global compte
    global investement
    global stock
    global invest_money
    global MONEY_SCRAPPERS
    global Entry_text
    global var_invest
    global var_compte
    global var_stock
    
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
            if MONEY_SCRAPPERS[invest_money].invest != 0 :
                MONEY_SCRAPPERS[invest_money].invest=MONEY_SCRAPPERS[invest_money].invest+int(Entry_text.get())
                MONEY_SCRAPPERS[invest_money].compte=MONEY_SCRAPPERS[invest_money].compte-int(Entry_text.get())
                
            elif MONEY_SCRAPPERS[invest_money].invest == 0:
                MONEY_SCRAPPERS[invest_money].stock_invest=MONEY_SCRAPPERS[invest_money].stock_invest.invest+int(Entry_text.get())
                MONEY_SCRAPPERS[invest_money].compte=MONEY_SCRAPPERS[invest_money].compte-int(Entry_text.get())
            
        if flag==False:
            MONEY_SCRAPPERS[invest_money].thread_flag_invest=flag
            
            if MONEY_SCRAPPERS[invest_money].invest != 0 :
                compte=MONEY_SCRAPPERS[invest_money].invest+MONEY_SCRAPPERS[invest_money].compte
                MONEY_SCRAPPERS[invest_money].compte=compte
            elif MONEY_SCRAPPERS[invest_money].invest == 0:
                compte=MONEY_SCRAPPERS[invest_money].stock_invest+MONEY_SCRAPPERS[invest_money].compte
                MONEY_SCRAPPERS[invest_money].compte=compte
            
            investement=0 
            MONEY_SCRAPPERS[invest_money].invest=0
            
            stock=0
            MONEY_SCRAPPERS[invest_money].stock_invest=0 
            
    else :
        tk.messagebox.showinfo("Attention", "Vous devez choisir une monnaie")
        
        
def plot(*args):
    global invest_money
    global compte
    global investement
    global stock
    global MONEY_SCRAPPERS
    global var_invest
    global var_compte
    global var_stock
    
    while MONEY_SCRAPPERS[invest_money].thread_flag_invest == True :
        var_invest.set(str(MONEY_SCRAPPERS[invest_money].invest))
        investement=MONEY_SCRAPPERS[invest_money].invest
        var_compte.set(str(MONEY_SCRAPPERS[invest_money].compte))
        compte=MONEY_SCRAPPERS[invest_money].compte
        var_stock.set(str(MONEY_SCRAPPERS[invest_money].stock_invest))
        stock=MONEY_SCRAPPERS[invest_money].stock_invest
        
    var_invest.set(str(investement))
    var_compte.set(str(compte))
    var_stock.set(str(stock))
       

def choose_money_invest(money):
    global invest_money
    global subplot_to_display
    
    for ax in fig_invest.get_axes():
        fig_invest.delaxes(ax)
    
    subplot_to_display=[]
    subplot_to_display.append(fig_invest.add_subplot(1,1,1))

    invest_money=money
    Thread(target=MONEY_SCRAPPERS[money].start_and_stop_scrap, args=(1,)).start() 
    refresh()

def set_mode(mode_choosen):
    global MODE
    global frame_Home
    global invest_Frame
    global compare_plot
    global invest_Frame
    
    MODE=mode_choosen
    
    frame_Home.pack_forget()
    
    if MODE==1:
        invest_Frame.pack(fill='both',side="top",expand=True)
    elif MODE==2:
        compare_plot.pack(fill='both',expand=True)


#---- CREATE AND FILL APP ----
    
app = tk.Tk()
app.title('VisioCrypto')
app.wm_iconbitmap('icon.ico')
    
compare_plot=tk.Frame(app) 
invest_Frame=tk.Frame(app)

#======================HOME INTERFACE==================================================
frame_Home=tk.Frame(app)

img_button_inv= tk.PhotoImage(file="gold_button_inv.png", master = frame_Home)
img_button_comp = tk.PhotoImage(file="gold_button_comp.png", master = frame_Home)
img_comp=tk.PhotoImage(file="compare.png", master = frame_Home)
img_inv=tk.PhotoImage(file="invest.png", master = frame_Home)

frame_choice_invest = tk.Frame(frame_Home)
frame_choice_invest.pack(side=tk.LEFT, fill=tk.BOTH, expand = True)

frame_choice_compare = tk.Frame(frame_Home)
frame_choice_compare.pack(side=tk.RIGHT, fill=tk.BOTH, expand = True)

button_compare = tk.Button(frame_choice_compare, text="Compare cryptocurrency", bd=0,command=partial(set_mode,2))
button_compare.config(image=img_comp)
button_invest = tk.Button(frame_choice_invest, text="Invest in cryptocurrency", bd=0,command=partial(set_mode,1))
button_invest.config(image=img_inv)

button_compare.pack(side=tk.RIGHT, fill=tk.BOTH, expand = True)
button_invest.pack(side=tk.LEFT, fill=tk.BOTH, expand = True)

frame_Home.pack(fill='both',expand=True)

#======================CANVAS==================================================

graphic=tk.Frame(compare_plot)
fig_compare_plot = Figure()
canvas = FigureCanvasTkAgg(fig_compare_plot, master=graphic)  # A tk.DrawingArea.
canvas.get_tk_widget().pack(fill="both", expand=True)
graphic.pack(fill='both',side='left',expand=True)

invest_plot=tk.Frame(invest_Frame)
graphic_invest=tk.Frame(invest_plot)
fig_invest = Figure()
canvas_invest = FigureCanvasTkAgg(fig_invest, master=invest_plot)  # A tk.DrawingArea.
canvas_invest.get_tk_widget().pack(fill="both", expand=True)
graphic_invest.pack(fill='both',side='left',expand=True)


#===================PARTIE INVEST==============================================

checkbox_invest=tk.Frame(invest_Frame) #Frame will contain all checkbox for invest
checkbox_container=[] #list will contain checkbox for invest
frame_my_money=tk.Frame(invest_Frame)#banner will contain ou money and our investement  


var1_invest=tk.StringVar()
var2_invest=tk.StringVar()
var3_invest=tk.StringVar()
var4_invest=tk.StringVar()
var5_invest=tk.StringVar()
var6_invest=tk.StringVar()
var7_invest=tk.StringVar()
var8_invest=tk.StringVar()

checkbox_container.append(tk.Checkbutton(checkbox_invest, text='Bitcoin', variable=var1_invest, onvalue=1, offvalue=0, command=partial(choose_money_invest, MONEY[0])))
checkbox_container.append(tk.Checkbutton(checkbox_invest, text='Ethereum', variable=var2_invest, onvalue=1, offvalue=0, command=partial(choose_money_invest, MONEY[1])))
checkbox_container.append(tk.Checkbutton(checkbox_invest, text='Litecoin', variable=var3_invest, onvalue=1, offvalue=0, command=partial(choose_money_invest, MONEY[2])))
checkbox_container.append(tk.Checkbutton(checkbox_invest, text='Monero', variable=var4_invest, onvalue=1, offvalue=0, command=partial(choose_money_invest, MONEY[3])))
checkbox_container.append(tk.Checkbutton(checkbox_invest, text='EOS', variable=var5_invest, onvalue=1, offvalue=0, command=partial(choose_money_invest, MONEY[4])))
checkbox_container.append(tk.Checkbutton(checkbox_invest, text='ATOM', variable=var6_invest, onvalue=1, offvalue=0, command=partial(choose_money_invest, MONEY[5])))
checkbox_container.append(tk.Checkbutton(checkbox_invest, text='Dash', variable=var7_invest, onvalue=1, offvalue=0, command=partial(choose_money_invest, MONEY[6])))
checkbox_container.append(tk.Checkbutton(checkbox_invest, text='WAVES', variable=var8_invest, onvalue=1, offvalue=0, command=partial(choose_money_invest, MONEY[7])))

for checkbox in checkbox_container:
    checkbox.deselect()
    checkbox.pack(fill='both',side="top",expand=True)

var_compte = tk.StringVar()
var_compte.set(str(compte))

label_account=tk.Label(frame_my_money,text='Compte :',pady=10,padx=10)
label_var_account=tk.Label(frame_my_money,textvariable =var_compte,pady=10)

label_account.pack(side='left')
label_var_account.pack(side='left')

var_invest = tk.StringVar()
var_invest.set(str(investement))

label_my_invest=tk.Label(frame_my_money,text='Invest :',pady=10,padx=10)
label_var_my_invest=tk.Label(frame_my_money,textvariable=var_invest,pady=10)

label_my_invest.pack(side='left')
label_var_my_invest.pack(side='left')

var_stock = tk.StringVar()
var_stock.set('0')

label_my_stock=tk.Label(frame_my_money,text='Stock :',pady=10,padx=10)
label_var_my_stock=tk.Label(frame_my_money,textvariable=var_stock,pady=10)

label_my_stock.pack(side='left')
label_var_my_stock.pack(side='left')

button_stop_invest = tk.Button(frame_my_money, text='Stop',command=partial(invest,False),padx=10)
button_stop_invest.pack( side = 'right')

button_go_invest = tk.Button(frame_my_money, text='Go',command=partial(invest,True),padx=10)
button_go_invest.pack( side = 'right')

Entry_text = tk.StringVar()
Entry_text.set('')

Entry_money_invest = tk.Entry(frame_my_money,textvariable=Entry_text)
Entry_money_invest.pack(side = 'right')

Label_money_invest = tk.Label(frame_my_money, text="Add :",padx=10, pady=10)
Label_money_invest.pack( side = 'right')


frame_my_money.pack(fill='x',side="top")
checkbox_invest.pack(fill='y',side="right")
invest_plot.pack(fill='both',side="left",expand=True)


#===================PARTIE MULTIPLOT======================================================

button_widget=tk.Frame(compare_plot)

var1=tk.StringVar()
var2=tk.StringVar()
var3=tk.StringVar()
var4=tk.StringVar()
var5=tk.StringVar()
var6=tk.StringVar()
var7=tk.StringVar()
var8=tk.StringVar()

#On défnit chaque boutton pour chaque monnaie avec comme paramètre le nom de la monnaie 

button_btc = tk.Checkbutton(button_widget, text='Bitcoin', variable=var1, onvalue="BTC", command=get_checked_button)
button_eth = tk.Checkbutton(button_widget, text='Ethereum', variable=var2, onvalue="ETH", command=get_checked_button)
button_ltc = tk.Checkbutton(button_widget, text='Litecoin', variable=var3, onvalue="LTC", command=get_checked_button)
button_mon = tk.Checkbutton(button_widget, text='Monero', variable=var4, onvalue="MLN", command=get_checked_button)
button_rip = tk.Checkbutton(button_widget, text='EOS', variable=var5, onvalue="EOS", command=get_checked_button)
button_car = tk.Checkbutton(button_widget, text='ATOM', variable=var6, onvalue="ATOM", command=get_checked_button)
button_das = tk.Checkbutton(button_widget, text='DASH', variable=var7, onvalue="DASH", command=get_checked_button)
button_lib = tk.Checkbutton(button_widget, text='WAVES', variable=var8, onvalue="WAVES", command=get_checked_button)
button_list = [button_btc, button_eth, button_ltc, button_mon, button_rip, button_car, button_das, button_lib]

for button in button_list:
    button.deselect()
    button['indicatoron'] = 0 
    button.pack(fill='both',expand=True,side="top")


button_widget.pack(fill='y',side="right")


app.mainloop()

for scrapper in MONEY:
    Thread(target=MONEY_SCRAPPERS[scrapper].destroy(), args=(1,)).start()
    time.sleep(1)




