# -*- coding: utf-8 -*-
"""
Created on Fri May  8 15:58:23 2020

@author: Aurélien
"""
from threading import Thread
import pandas as pd
from datetime import datetime, timedelta
import csv
import os.path
import time
from selenium import webdriver
from functools import partial
from statistics import mean

class Scrapper :
    
    PAUSE=10
    
    def __init__(self,name):
        
        try:
            self.driver=webdriver.Firefox(executable_path=r'./geckodriver/geckodriver.exe')
        except:
            try :
               self.driver=webdriver.Chrome(executable_path=r'./chromedriver80/chromedriver.exe') 
            except :
                try :
                   self.driver=webdriver.Chrome(executable_path=r'./chromedriver81/chromedriver.exe') 
                except :
                    try :
                       self.driver=webdriver.Chrome(executable_path=r'./chromedriver83/chromedriver.exe') 
                    except :
                        print('No Driver Available')
                        
        self.started=False
        self.name=name
        self.thread_flag=False
        self.thread_flag_invest=False
        self.invest=0
        self.compte=0
        self.first_invest=0
        self.filename=str(self.name+'.csv')
        self.file_exists = os.path.isfile(self.filename)
        thread_selenium = Thread(target=partial(self.init_selenium,Scrapper), args=(1,))
        thread_selenium.start()
        self.dataFrame=pd.DataFrame({'Value':[],'Date':[]})
        """
        if self.file_exists :
            
            self.dataFrame=pd.read_csv(self.filename,sep="/").reset_index(drop=True)
            self.dataFrame["Date"] = self.dataFrame["Date"].astype(str)
            self.dataFrame["Date"] = self.dataFrame["Date"].apply(lambda x: datetime.fromisoformat(x))
            
        else :
            
            self.dataFrame=pd.DataFrame({'Value':[],'Date':[]})
        """           
                              
    def destroy(self,*args):
        
        self.thread_flag=False
        self.thread_flag_invest=False
        self.driver.close()
        self.filling_csv()
        
        
    def close_tab(self):
        
        self.driver.quit()
        
    
    def init_selenium(self,*args):
        
        self.url=str('https://trade.kraken.com/fr-fr/charts/KRAKEN:'+self.name+'-EUR')
        self.driver.get(self.url)
        
    
    def start_and_stop_scrap(self,*args):
        
        if self.thread_flag==False:
            self.thread_flag=True
            thread_scrap = Thread(target=self.get_data, args=(1,))
            thread_scrap.start()
            
        else :
            self.thread_flag=False
            
    def start_and_stop_invest(self,my_money,my_invest,flag,*args):
        self.first_invest= my_invest
        self.invest=my_invest/self.dataFrame['Value'][self.dataFrame.shape[0]-1]
        print(self.dataFrame['Value'][self.dataFrame.shape[0]-1])
        self.compte=my_money
        thread_invest = Thread(target=partial(self.invest_my_money,my_money,my_invest), args=(1,))
        thread_invest.start()
    
    def invest_my_money(self,*args):
        
        value_max=0
        value_min=0
        invest_init=0
        invest_on_compte=0
        
        while self.thread_flag_invest==True :
            print(self.invest*self.dataFrame['Value'][self.dataFrame.shape[0]-1])
            """
            if self.dataFrame['Value'][self.dataFrame.shape[0]-1]>self.dataFrame['Value'][self.dataFrame.shape[0]-2] :
                if self.dataFrame['Value'][self.dataFrame.shape[0]-1]>value_max : 
                    value_max=self.dataFrame['Value'][self.dataFrame.shape[0]-1]
            """
            time.sleep(Scrapper.PAUSE)
    
    #Fonction qui va scrapper la donnée 
    def get_data(self,*args):
        
        while self.thread_flag==True :
        
            time_start=time.process_time()
            price=self.driver.find_element_by_id("price-ticker").find_elements_by_tag_name('span')[1]

            if self.dataFrame.shape[0] > 3:
                self.dataFrame.loc[self.dataFrame.shape[0]-1]=[float(price.text[:-4]),datetime.now()]
                time_n1= datetime.now() + timedelta(0, 10, 0)
                predict=mean(self.dataFrame['Value'][-2:].to_list())
                self.dataFrame.loc[self.dataFrame.shape[0]]=[float(predict),time_n1]
                
            elif self.dataFrame.shape[0] == 2 :
                self.dataFrame.loc[self.dataFrame.shape[0]]=[float(price.text[:-4]),datetime.now()]
                time_n1= datetime.now() + timedelta(0, 10, 0)
                predict=mean(self.dataFrame['Value'][-2:].to_list())   
                self.dataFrame.loc[self.dataFrame.shape[0]]=[float(predict),time_n1]
                
            else:
                self.dataFrame.loc[self.dataFrame.shape[0]]=[float(price.text[:-4]),datetime.now()]
                
            time_stop=time.process_time()
            time.sleep(Scrapper.PAUSE-(time_stop-time_start))
    
    
    #Fonction qui va remplir le csv avec la dataFrame 
    def filling_csv (self):
        
        if self.file_exists :
            
            try :
                os.remove(self.filename)
                
            except:
                print('the file not exist')
                
        with open(self.filename, 'w', newline="") as csv_file:
            fieldnames = ["Value", "Date"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter="/")
            writer.writeheader()
            
            for row in self.dataFrame.itertuples() :
                writer.writerow({"Value" : row.Value, "Date" : row.Date})

        