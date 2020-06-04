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
        #choose the correct webdriver
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
        
        self.name=name #name of cryptomoney
        self.thread_flag_scrapping=False #flag for scrapping
        self.thread_flag_invest=False #flag for start or stop invest
        self.invest=0#value of the investiment accord to the value of the money
        self.compte=0#value of our money
        self.my_invest=0#value initial of the investement
        self.stock_invest=0# varaible will stock the money invested when the cryptomonney loose value
        self.filename=str(self.name+'.csv')#name of file .csv
        self.file_exists = os.path.isfile(self.filename)
        self.max_dataFrame=0
        thread_selenium = Thread(target=partial(self.init_selenium,Scrapper), args=(1,))
        thread_selenium.start()
        self.dataFrame=pd.DataFrame({'Value':[],'Date':[]})
        
        """ We have comment this part because actually is more interessant to see the data in live in our application 
        if self.file_exists :
            
            self.dataFrame=pd.read_csv(self.filename,sep="/").reset_index(drop=True)
            self.dataFrame["Date"] = self.dataFrame["Date"].astype(str)
            self.dataFrame["Date"] = self.dataFrame["Date"].apply(lambda x: datetime.fromisoformat(x))
            
        else :
            
            self.dataFrame=pd.DataFrame({'Value':[],'Date':[]})
        """           
                              
    def destroy(self,*args): #destroy all thread, close webdriver and fill csv

        self.thread_flag_invest=False
        self.driver.close()
        self.filling_csv()
    
    def init_selenium(self,*args): #initialisation of the web page with the url of the cryptomonnaie
        
        self.url=str('https://trade.kraken.com/fr-fr/charts/KRAKEN:'+self.name+'-EUR')
        self.driver.get(self.url)
        
    
    def start_and_stop_scrap(self,*args): #start or stop scrapping
        
        if self.thread_flag_scrapping==False:
            self.thread_flag_scrapping=True
            thread_scrap = Thread(target=self.get_data, args=(1,))
            thread_scrap.start()
            
        else :
            self.thread_flag_scrapping=False
            
    def start_and_stop_invest(self,my_money,my_invest,flag,*args):  #start or stop invest
        self.my_invest=my_invest/self.dataFrame['Value'][self.dataFrame.shape[0]-2]
        print("On a temps d'unité de crypto' : ",self.my_invest)
        self.invest=0
        print(self.dataFrame['Value'][self.dataFrame.shape[0]-1])
        self.compte=my_money
        thread_invest = Thread(target=self.invest_my_money, args=(1,))
        thread_invest.start()
    
    def invest_my_money(self,*args): #manage the money invest
        self.max_dataFrame=self.dataFrame['Value'][self.dataFrame.shape[0]-1]
        self.min_dataFrame=self.dataFrame['Value'][self.dataFrame.shape[0]-1]
        
        while self.thread_flag_invest==True :
            if self.dataFrame.shape[0] > 3:
            
                while self.dataFrame['Value'][self.dataFrame.shape[0]-1]<=self.max_dataFrame:
                    self.max_dataFrame=self.dataFrame['Value'][self.dataFrame.shape[0]-2]
                    self.invest=self.my_invest*self.dataFrame['Value'][self.dataFrame.shape[0]-2]
                    time.sleep(0.5)
                
                self.stock_invest=self.my_invest*self.dataFrame['Value'][self.dataFrame.shape[0]-2]
                self.my_invest=self.stock_invest
                self.invest=0
                
                self.min_dataFrame=self.dataFrame['Value'][self.dataFrame.shape[0]-2]
                
                while self.dataFrame['Value'][self.dataFrame.shape[0]-1]>=self.min_dataFrame:
                    self.min_dataFrame=self.dataFrame['Value'][self.dataFrame.shape[0]-2] 
                    time.sleep(0.5)
                
                self.my_invest=self.stock_invest/self.dataFrame['Value'][self.dataFrame.shape[0]-2]
                self.invest=self.my_invest*self.dataFrame['Value'][self.dataFrame.shape[0]-2]
                self.stock_invest=0
                
                print("On a temps d'unité de crypto' : ",self.my_invest)
                self.max_dataFrame=self.dataFrame['Value'][self.dataFrame.shape[0]-2]
            
    

    def get_data(self,*args): # while loop while stock the data of the scrapping
        
        while self.thread_flag_scrapping==True :
        
            time_start=time.process_time()
            
            price=self.driver.find_element_by_id("price-ticker").find_elements_by_tag_name('span')[1]

            if self.dataFrame.shape[0] > 3:
                self.dataFrame.loc[self.dataFrame.shape[0]-1]=[float(price.text[:-4]),datetime.now()]
                time_n1= datetime.now() + timedelta(0, 10, 0)
                predict=mean(self.dataFrame['Value'][-3:].to_list())
                self.dataFrame.loc[self.dataFrame.shape[0]]=[float(predict),time_n1]
                
            elif self.dataFrame.shape[0] == 2 :
                self.dataFrame.loc[self.dataFrame.shape[0]]=[float(price.text[:-4]),datetime.now()]
                time_n1= datetime.now() + timedelta(0, 10, 0)
                predict=mean(self.dataFrame['Value'][-3:].to_list())   
                self.dataFrame.loc[self.dataFrame.shape[0]]=[float(predict),time_n1]
                
            else:
                self.dataFrame.loc[self.dataFrame.shape[0]]=[float(price.text[:-4]),datetime.now()]
                

            time_stop=time.process_time()
            time.sleep(Scrapper.PAUSE-(time_stop-time_start))
    
    
    def filling_csv (self): # filling the csv with de dataFrame
        
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
