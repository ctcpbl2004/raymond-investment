# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 21:28:05 2018

@author: Raymond
"""
import DB_Connector
import Controller
from View import Custom_Object
from View import Font_Family

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import numpy as np
import pandas as pd


Color_fameily = {'Background':'#181818',
                 'Grey':'#282828',
                 'Chart': '#107B8C',
                 'custom_yellow':'#FF9C29'}



class MainWindow(tk.Tk):
    def __init__(self):
        self.root = tk.Tk()
        self.root.wm_title('Stock Viewer')
        self.root.geometry('1025x720')
        self.root.resizable(False, False)
        
        
        self.Top_Frame()
        self.Main_Frame()
        self.Right_Frame()
        self.Footer_Frame()
        #self.Initiate_customs_style()
        self.root.bind("<Return>", lambda event:self.Enter())
        self.root.mainloop()
    
    def Initiate_customs_style(self):
        
        style = ttk.Style()
        
        style.theme_create("Raymond", parent = "alt",
                           settings = {
                                   "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] ,'background' :"#181818"} },
                                    "TNotebook.Tab": {
                                            "configure": {"padding": [1, 1], "background": "#282828" ,'foreground':'white'},
                                            "map": {"background": [("selected", "#FF9C29")],
                                                    "foreground":[('selected','black')],
                                                    "expand": [("selected", [0, 0, 0, 0])]}} ,
                                    "Treeview":{"configure":{'background': Color_fameily['Grey'], 'foreground': 'white', 'selectbackground': '#FF9C29'}},
                                                "Option":{'selectmode':'browser'},
                                    "Treeview.Heading":{
                                            "configure":{'background': 'black', 'foreground':'white'}}
                                   })
        style.theme_use("Raymond")
    
    def Enter(self):
        Ticker = self.Ticker_Entry.get()
        data = DB_Connector.GetData.Equity(Ticker)[-2000:]
        self.Stock_Chart.clear()
        self.Stock_Chart.grid(True,color='white', alpha = 0.5, linestyle = '--',linewidth = 0.5)
        self.Stock_Chart.set_title(DB_Connector.GetData.Get_EquityName(Ticker) + ' (' + Ticker + ')',fontsize = 12, color = 'white')

        self.Stock_Chart.plot( data.index,data['AdjClose'] ,lw=0.5,color='white',alpha=1)
        self.Stock_Chart.fill_between(data.index, data['AdjClose'],facecolor = Color_fameily['Chart'])
        self.canvas.draw()
        
        data['Return'] = data['AdjClose'].pct_change()
        data['Std_22'] = data['Return'].rolling(22).std()*np.sqrt(252)*100.
        data['Std_44'] = data['Return'].rolling(44).std()*np.sqrt(252)*100.
        data['Std_66'] = data['Return'].rolling(66).std()*np.sqrt(252)*100.
        data['Std_252'] = data['Return'].rolling(252).std()*np.sqrt(252)*100.

        self.Volatility_Chart.clear()
        self.Volatility_Chart.grid(True,color='white', alpha = 0.5, linestyle = '--',linewidth = 0.5)
        self.Volatility_Chart.set_title("Volatility",fontsize = 10, color = 'white')
        self.Volatility_Chart.plot( data.index,data['Std_22'] ,lw=0.5,color='white',alpha=1)
        self.Volatility_Chart.plot( data.index,data['Std_44'] ,lw=0.5,color='white',alpha=1)
        self.Volatility_Chart.plot( data.index,data['Std_66'] ,lw=0.5,color='yellow',alpha=1)
        self.Volatility_Chart.plot( data.index,data['Std_252'] ,lw=0.5,color='red',alpha=1)
        self.canvas2.draw()
        
        
        
        
        
    
    def Top_Frame(self):
        
        
        self.Frame_Top = tk.Frame(self.root,width = 1025, height = 50,background = Color_fameily['Background'])
        self.Frame_Top.place(x = 0, y = 0)
               
        self.Ticker_Entry = Custom_Object.AutocompleteEntry(DB_Connector.GetData.Summary_table()['Ticker'].tolist(), self.Frame_Top, width = 40, bg = Color_fameily['custom_yellow'], font = Font_Family.Font_family['Normal'])
        self.Ticker_Entry.place(x = 10, y = 10)
        
        self.Enter_Button = tk.Button(self.Frame_Top,width=15, text =u"  Enter  ",command = self.Enter,font = Font_Family.Font_family['Normal'],relief='raised',fg='white',bg='black',activebackground='#FF9C29')
        self.Enter_Button.place(x = 400, y = 10)
        
    def Main_Frame(self):
        self.Frame_Main = tk.Frame(self.root,width = 800, height = 480,background = Color_fameily['Background'])
        self.Frame_Main.place(x = 0, y = 50)

        self.fig = Figure(figsize=(6,4), dpi=120)
        self.fig.set_tight_layout(True)
        self.fig.patch.set_facecolor(Color_fameily['Background'])
        
        self.Stock_Chart = self.fig.add_subplot(111,facecolor='#213139')
        self.Stock_Chart.tick_params(axis='both', which='major', labelsize=8)
        #self.Stock_Chart.set_xlabel('Simulation Time', fontsize=10)
        #self.Stock_Chart.set_ylabel('Stock price', fontsize=10)
        self.Stock_Chart.grid(True,color='white', alpha = 0.5, linestyle = '--',linewidth = 0.5)
        self.Stock_Chart.tick_params(axis='both', which='major',colors='white', labelsize=6)
        self.Stock_Chart.spines['bottom'].set_color('white')
        self.Stock_Chart.spines['top'].set_color('white')
        self.Stock_Chart.spines['left'].set_color('white')
        self.Stock_Chart.spines['right'].set_color('white')
        self.Stock_Chart.xaxis.label.set_color('white')
        self.Stock_Chart.yaxis.label.set_color('white')


        self.canvas = FigureCanvasTkAgg(self.fig, master=self.Frame_Main)
        self.canvas.get_tk_widget().place(x=10,y=0)
        self.canvas.get_tk_widget().configure(background='#000000',  highlightcolor='#FFFFFF', highlightbackground='#FFFFFF')
        
    def Right_Frame(self):
        self.Frame_Right = tk.Frame(self.root,width = 800, height = 720,background = Color_fameily['Background'])
        self.Frame_Right.place(x = 800, y = 50)
        

    def Footer_Frame(self):
        self.Frame_Footer = tk.Frame(self.root,width = 800, height = 200,background = Color_fameily['Background'])
        self.Frame_Footer.place(x = 0, y = 530)

        self.fig2 = Figure(figsize=(7.25,2), dpi=100)
        self.fig2.set_tight_layout(True)
        self.fig2.patch.set_facecolor(Color_fameily['Background'])
        
        self.Volatility_Chart = self.fig2.add_subplot(111,facecolor='#213139')
        self.Volatility_Chart.tick_params(axis='both', which='major', labelsize=8)
        #self.Volatility_Chart.set_xlabel('Time', fontsize=10)
        self.Volatility_Chart.set_ylabel('Volatility(%)', fontsize=10)
        self.Volatility_Chart.set_title("Volatility",fontsize = 10, color = 'white')
        self.Volatility_Chart.grid(True,color='white', alpha = 0.5, linestyle = '--',linewidth = 0.5)
        self.Volatility_Chart.tick_params(axis='both', which='major',colors='white', labelsize=6)
        self.Volatility_Chart.spines['bottom'].set_color('white')
        self.Volatility_Chart.spines['top'].set_color('white')
        self.Volatility_Chart.spines['left'].set_color('white')
        self.Volatility_Chart.spines['right'].set_color('white')
        self.Volatility_Chart.xaxis.label.set_color('white')
        self.Volatility_Chart.yaxis.label.set_color('white')
        
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.Frame_Footer)
        self.canvas2.get_tk_widget().place(x=0,y=0)
        self.canvas2.get_tk_widget().configure(background='#000000',  highlightcolor='#FFFFFF', highlightbackground='#FFFFFF')


if __name__ == "__main__":
    app = MainWindow()
