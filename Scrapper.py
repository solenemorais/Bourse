# -*- coding: utf-8 -*-
"""
Created on Fri May  8 15:58:23 2020

@author: Aurélien
"""
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

class Scrapper :
    
    PAUSE=10
    
    def __init__(self,name):
        
        self.started=False
        self.name=name
        self.thread_flag=False
        self.filename=str(self.name+'.csv')
        self.file_exists = os.path.isfile(self.filename)
        
        if self.file_exists :
            self.dataFrame=pd.read_csv(self.filename,sep="/").reset_index(drop=True)
            self.dataFrame["Date"] = df["Date"].astype(str)
            self.dataFrame["Date"] = df["Date"].apply(lambda x: datetime.fromisoformat(x))
        else :
            self.dataFrame={'Value':[],'Date':[]}

    def start_and_stop(self):
        if self.thread_flag==False:
            self.thread_flag==True
            thread_scrap = Thread(target=self.get_data(), args=(1,))
            thread_scrap.start()
        else:
            self.thread_flag==False
        
    
    #Fonction qui va scrapper la donnée 
    def get_data(self):
        driver=webdriver.Firefox()
        url=str('https://trade.kraken.com/fr-fr/charts/KRAKEN:'+self.name+'-EUR')
        driver.get(url)
        
        while self.thread_flag==True :
            time_start=time.process()
            price=driver.find_element_by_id("price-ticker").find_elements_by_tag_name('span')[1]
            print(price)
            self.dataFrame.loc[df.shape[0]]=[float(price.text[:-4]),datetime.now()]
            time_stop=time.process()
            time.sleep(Scrapper.PAUSE-(time_stop-time_start))
    
    
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
        