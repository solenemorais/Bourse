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

url="https://www.boursorama.com/bourse/devises/taux-de-change-bitcoin-euro-BTC-EUR/"
dataFrame=pd.DataFrame({'data':[],'date':[],'time':[]})
i=0
while (1):
    timeA=time.process_time_ns()
    page=requests.get(url)
    soup=BeautifulSoup(page.text,'lxml')
    element=soup.find('span',{"class":"c-instrument c-instrument--last"})
    local_time=time.localtime()
    date=str(local_time.tm_mday)+"/"+str(local_time.tm_mon)+"/"+str(local_time.tm_year)
    heure=str(local_time.tm_hour)+":"+str(local_time.tm_min)+":"+str(local_time.tm_sec)
    dataFrame.loc[i]=[element.text,date,heure]
    i+=1
    plt.plot(dataFrame.time,dataFrame.data)
    plt.xticks(dataFrame.time,rotation=45)
    plt.show()
    dataFrame.to_excel("output.xlsx")
    timeB=time.process_time_ns()
    time.sleep(5-(timeB-timeA)/1000000000)
    
    
