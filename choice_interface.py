# -*- coding: utf-8 -*-
"""
Created on Tue May 12 18:26:43 2020

@author: solen
"""

import tkinter as tk
app = tk.Tk()

img_button_inv= tk.PhotoImage(file="gold_button_inv.png", master = app)
img_button_comp = tk.PhotoImage(file="gold_button_comp.png", master = app)
img_comp=tk.PhotoImage(file="compare.png", master = app)
img_inv=tk.PhotoImage(file="invest.png", master = app)
#img_canv_inv=


frame_choice_invest = tk.Frame(app)
frame_choice_invest.pack(side=tk.LEFT, fill=tk.BOTH, expand = True)

frame_choice_compare = tk.Frame(app)
frame_choice_compare.pack(side=tk.RIGHT, fill=tk.BOTH, expand = True)


#background_label = tk.Label(frame_choice_compare, image=img_comp)


#canvas_inv=tk.Canvas(frame_choice_invest)
#canvas_inv.pack(expand=tk.YES, fill=tk.BOTH)
#canvas_comp=tk.Canvas(frame_choice_compare)
#canvas_comp.create_image(0,0, anchor=tk.NW, image=img_canv_comp)
#canvas_comp.pack(expand=tk.YES, fill=tk.BOTH)

button_compare = tk.Button(frame_choice_compare, text="Compare cryptocurrency", bd=0)
button_compare.config(image=img_comp)
button_invest = tk.Button(frame_choice_invest, text="Invest in cryptocurrency", bd=0)
button_invest.config(image=img_inv)

#background_label.pack()
button_compare.pack(side=tk.RIGHT, fill=tk.BOTH, expand = True)
button_invest.pack(side=tk.LEFT, fill=tk.BOTH, expand = True)

app.mainloop()

