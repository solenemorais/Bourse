# -*- coding: utf-8 -*-
"""
Created on Fri May  8 15:58:23 2020

@author: Aurélien
"""
from threading import Thread
import pandas as pd
from datetime import datetime
import csv
import os.path
import time
from selenium import webdriver
from functools import partial


class Scrapper :
    
    PAUSE=10
    
    def __init__(self,name):
        try:
            self.driver=webdriver.Firefox('./geckodriver')
        except:
            try :
               self.driver=webdriver.Chrome('./chromedriver80') 
            except :
                try :
                   self.driver=webdriver.Chrome('./chromedriver81') 
                except :
                    try :
                       self.driver=webdriver.Chrome('./chromedriver83') 
                    except :
                        print('No Driver Available')
        self.started=False
        self.name=name
        self.thread_flag=False
        self.filename=str(self.name+'.csv')
        self.file_exists = os.path.isfile(self.filename)
        thread_selenium = Thread(target=partial(self.init_selenium,Scrapper), args=(1,))
        thread_selenium.start()
        if self.file_exists :
            self.dataFrame=pd.read_csv(self.filename,sep="/").reset_index(drop=True)
            self.dataFrame["Date"] = self.dataFrame["Date"].astype(str)
            self.dataFrame["Date"] = self.dataFrame["Date"].apply(lambda x: datetime.fromisoformat(x))
        else :
            self.dataFrame=pd.DataFrame({'Value':[],'Date':[]})
                              
    def destroy_thread(self,*args):
        self.thread_flag=False
        self.driver.close()
        
    def close_tab(self):
        self.driver.close()
    
    def init_selenium(self,*args):
        self.url=str('https://trade.kraken.com/fr-fr/charts/KRAKEN:'+self.name+'-EUR')
        self.driver.get(self.url)
    
    def start_and_stop(self,*args):
        if self.thread_flag==False:
            self.thread_flag=True
            thread_scrap = Thread(target=self.get_data(), args=(1,))
            thread_scrap.start()
        else :
            self.thread_flag=False
        
    
    #Fonction qui va scrapper la donnée 
    def get_data(self):
        while self.thread_flag==True :
            time_start=time.process_time()
            price=self.driver.find_element_by_id("price-ticker").find_elements_by_tag_name('span')[1]
            print(price)
            self.dataFrame.loc[self.dataFrame.shape[0]]=[float(price.text[:-4]),datetime.now()]
            time_stop=time.process_time()
            time.sleep(Scrapper.PAUSE-(time_stop-time_start))
    
    
    #Fonction qui va remplir le csv avec la dataFrame 
    def filling_csv (self):
        if self.file_exists :
            os.remove(self.filename)
        with open(self.filename, 'w', newline="") as csv_file:
            fieldnames = ["Value", "Date"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter="/")
            writer.writeheader()
            for row in self.dataFrame.itertuples() :
                writer.writerow({"Value" : row.Value, "Date" : row.Date})

        