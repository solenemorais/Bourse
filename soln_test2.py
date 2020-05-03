# -*- coding: utf-8 -*-
"""
Created on Sun May  3 17:21:02 2020

@author: solen
"""
"""
import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def plotting_data():
    #---- READ THE CSV ----
    plt.style.use('fivethirtyeight')

    def animate(i):
        data = pd.read_csv('scrape_data.csv')
        x = data['Heure']
        y = data['Valeur']
        
        #clear the axes:
        plt.cla()
                    
        plt.plot(x, y, label='Channel 1')
        
        plt.legend(loc='upper left')
        plt.tight_layout()

    FuncAnimation(plt.gcf(), animate, interval=1000)
    
    plt.tight_layout()
    plt.show()

plotting_data()


"""
#plt.style.use('fivethirtyeight')

x_vals = []
y_vals = []


index = count()


def animate(i):
    x_vals.append(next(index))
    y_vals.append(random.randint(0,5))
    
    plt.plot(x_vals, y_vals)


#gcf:getcurrentfigure
ani = FuncAnimation(plt.gcf(), animate, interval=1000)

# index = count()

# def animate(i):
#     x_vals.append(next(index))
#     y_vals.append(random.randint(0, 5))


plt.tight_layout()
plt.show()


# data = pd.read_csv('data.csv')
# x = data['x_value']
# y1 = data['total_1']
# y2 = data['total_2']
