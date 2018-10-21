# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 11:34:04 2018

@author: Raymond
"""

import DB_Connector
import Controller
import tkinter as tk
from tkinter import ttk
import numpy as np


Font_family = {'Large':("Arial",16,'bold'),
               'Title':("Arial",20,'bold')}

Color_fameily = {'Background':'#181818',
                 'Grey':'#282828',
                 'Chart': ''}

'''
                                    "Treeview":{"configure":{'background': Color_fameily['Grey'], 'foreground': 'white'}, 'selectbackground': '#FF9C29'},
                                    "Treeview.Heading":{
                                            "configure":{'background': 'black', 'foreground':'white'}}

'''














class MainWindow(tk.Tk):
    def __init__(self):
        self.root = tk.Tk()
        self.root.wm_title('Stock Viewer')
        self.root.geometry('1600x600')
        self.root.resizable(False, False)
        
        self.Right_Frame()
        
        self.Top_Frame()

        self.Main_Frame()
        
        self.Footer_Frame()
        self.Initiate_customs_style()
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
    
    def Top_Frame(self):
        self.Frame_Top = tk.Frame(self.root,width = 800, height = 100,background = Color_fameily['Background'])
        self.Frame_Top.place(x = 0, y = 0)
        
        Label1 = tk.Label(self.Frame_Top, text = 'test', font = Font_family['Large'], fg = 'white', background = Color_fameily['Background'])
        Label1.place(x = 10, y = 10)
        
    def Main_Frame(self):
        self.Frame_Main = tk.Frame(self.root,width = 800, height = 400,background = Color_fameily['Background'])
        self.Frame_Main.place(x = 0, y = 100)
        '''
        style = ttk.Style()
        
        style.theme_create("Raymond", parent = "alt",
                           settings = {
                                   "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] ,'background' :"#181818"} },
                                    "TNotebook.Tab": {
                                            "configure": {"padding": [1, 1], "background": "#282828" ,'foreground':'white'},
                                            "map": {"background": [("selected", "#FF9C29")],
                                                    "foreground":[('selected','black')],
                                                    "expand": [("selected", [0, 0, 0, 0])]}} ,
                                    "Treeview":{"configure":{'background': Color_fameily['Grey'], 'foreground': 'white'}}
                                   })
        
        style.theme_use("Raymond")
        '''
        Notebook = ttk.Notebook(self.Frame_Main, width = 700, height = 300)
        Notebook.place(x = 50, y = 50)
        
        Frame1 = tk.Frame(Notebook,width = 200, height = 100, background = 'red')
        Frame2 = tk.Frame(Notebook,width = 200, height = 100, background = 'green')
        
        Notebook.add(Frame1, text = "--1--")
        Notebook.add(Frame2, text = "--2--")
        
    def Right_Frame(self):
        self.Frame_Right = tk.Frame(self.root,width = 800, height = 400,background = Color_fameily['Background'])
        self.Frame_Right.place(x = 800, y = 100)
        
        Tree_table = ttk.Treeview(self.Frame_Right, height = "10")
        
        Tree_table["columns"]=("column1","column2",'column3')
        Tree_table.column("#0",width=10, anchor='e')
        Tree_table.column("column1", width=80, anchor='center' )
        Tree_table.column("column2", width=60, anchor='center')
        Tree_table.column("column3", width=80 , anchor='center')


        Tree_table.heading('#0', text='')
        Tree_table.heading("column1", text="Date")
        Tree_table.heading("column2", text="Signal")
        Tree_table.heading("column3", text="Price")

        Tree_table.place(x=10, y=10)


        for i in range(20):
            Tree_table.insert("",i,text=str(i),values=(np.random.lognormal(size=1)[0],np.random.lognormal(size=1)[0],np.random.lognormal(size=1)[0]))        
        
        

    def Footer_Frame(self):
        self.Frame_Footer = tk.Frame(self.root,width = 800, height = 100,background = Color_fameily['Background'])
        self.Frame_Footer.place(x = 0, y = 500)

if __name__ == "__main__":
    app = MainWindow()
