# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 14:54:07 2020

@author: Aurélien
"""

import requests
from bs4 import BeautifulSoup 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import time
import os 

url="https://coinmarketcap.com/currencies/bitcoin/"


if os.path.exists('output.xlsx') == True:
    dataFrame_excel=pd.read_excel('output.xlsx')
    dataFrame=pd.DataFrame({'data':dataFrame_excel.data,'date':dataFrame_excel.date,'time':dataFrame_excel.time,'time_h_min':dataFrame_excel.time_h_min,'time_h':dataFrame_excel.time_h,'day':dataFrame_excel.day,'min':dataFrame_excel.min,'hour':dataFrame_excel.hour,'mday':dataFrame_excel.mday})
    i=len(dataFrame)+1
else:
    dataFrame=pd.DataFrame({'data':[],'date':[],'time':[],'time_h_min':[],'time_h':[],'day':[],'min':[],'hour':[],'mday':[]})
    i=0

while (1):
    timeA=time.process_time()
    
    local_time=time.localtime()
    date=str(local_time.tm_mday)+"/"+str(local_time.tm_mon)+"/"+str(local_time.tm_year)
    time_h_min_sec=str(local_time.tm_hour)+":"+str(local_time.tm_min)+":"+str(local_time.tm_sec)
    time_h_min=str(local_time.tm_hour)+":"+str(local_time.tm_min)
    time_h=str(local_time.tm_hour)
    day=str(local_time.tm_mday)+"/"+str(local_time.tm_mon)
    
    page=requests.get(url)
    soup=BeautifulSoup(page.text,'lxml')
    element=soup.find('div',{"class":"cmc-details-panel-about__table"}).find_all('div')   
    dataFrame.loc[i]=[float(element[2].text[1:-4].replace('.','').replace(',','.')),date,time_h_min_sec,time_h_min,time_h,day,local_time.tm_min,local_time.tm_hour,local_time.tm_mday]
    
    plt.title("Cours BTC")
    plt.ylabel('Valeur BTC-USD')
    plt.xlabel('Heure')
    plt.plot(dataFrame.data,color='orange')
    
    if dataFrame.loc[0].min == local_time.tm_min+10 :
        xlabels=dataFrame.time.unique()
        plt.xticks(dataFrame.time,rotation=45)
    elif dataFrame.loc[0].hour==local_time.tm_hour:
        xlabels=dataFrame.time_h_min.unique()
        plt.xticks(np.arange(0,dataFrame.shape[0],step=dataFrame.shape[0]/len(xlabels)),xlabels,rotation=45)
    elif (dataFrame.loc[0].hour+3) > local_time.tm_hour:
        xlabels=dataFrame.time_h_min.unique()
        for element in xlabels:
            if element[-1]!='0':
                xlabels[np.where(xlabels == element)]=element[0:3]+element[-1].replace(element[-1],'0')
        xlabels=np.unique(xlabels)   
        plt.xticks(np.arange(0,dataFrame.shape[0],step=dataFrame.shape[0]/len(xlabels)),xlabels,rotation=45)
    else :
        xlabels=dataFrame.time_h.unique()[:-1]
        plt.xticks(np.arange(0,dataFrame.shape[0],step=dataFrame.shape[0]/len(xlabels)),xlabels,rotation=45)
    plt.show()
    dataFrame.to_excel("output.xlsx")
    i+=1
    timeB=time.process_time()
    time.sleep(20-(timeB-timeA))
    

    
