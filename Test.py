import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.figure
import matplotlib.backends.backend_tkagg
import numpy as np
import tkinter as tk
import requests
from bs4 import BeautifulSoup 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import os 

def on_key_event(event, canvas, toolbar):
    matplotlib.backend_bases.key_press_handler(event, canvas, toolbar)

url="https://coinmarketcap.com/currencies/bitcoin/"
dataFrame=pd.DataFrame({'data':[],'date':[],'time':[],'time_h_min':[],'time_h':[],'day':[],'min':[],'hour':[],'mday':[]})
i=0  

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

matplotlib.use('TkAgg')
root = tk.Tk()
root.wm_title('Test window')
fig = matplotlib.figure.Figure(figsize=(9.333, 7), dpi=100)
a = fig.add_subplot(111)
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.X, expand=1)
canvas.mpl_connect(
    'key_press_event',
    lambda event: on_key_event(event, canvas, toolbar)
)
toolbar = matplotlib.backends.backend_tkagg.NavigationToolbar2Tk(
    canvas, root
)
toolbar.update()
root.bind('<Control-w>', lambda event: root.destroy())
tk.mainloop()