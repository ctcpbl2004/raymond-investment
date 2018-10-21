# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 12:02:20 2018

@author: Raymond
"""
import tkinter as tk
import re
from View import Font_Family


class AutocompleteEntry(tk.Entry):
    def __init__(self, lista, *args, **kwargs):

        tk.Entry.__init__(self, *args, **kwargs)
        self.lista = lista       
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = tk.StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Return>", self.selection)
        self.bind("<Tab>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)
        self.bind("<Escape>", self.clear)
        #self.bind("<Leave>", self.clear)
        
        self.lb_up = False

    def changed(self, name, index, mode): 

        if self.var.get() == '':
            self.lb.destroy()
            self.lb_up = False
        else:
            words = self.comparison()
            if words:           
                if not self.lb_up:
                    self.lb = tk.Listbox(font=Font_Family.Font_family['Normal'],width = 40, background="#181818", fg="white",selectforeground='black',
                                         selectbackground="#FF9C29",highlightcolor="#181818",activestyle=tk.NONE)
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)
                    self.lb.place(x=self.winfo_x(), y=self.winfo_y()+self.winfo_height())
                    self.lb_up = True

                self.lb.delete(0, tk.END)
                for w in words:
                    self.lb.insert(tk.END,w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False
                    
    def clear(self, event):
        self.lb.destroy()
        self.lb_up = False
        self.icursor(tk.END)
        
    def selection(self, event):

        if self.lb_up:
            self.var.set(self.lb.get(tk.ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(tk.END)

    def up(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':               
                self.lb.selection_clear(first=index)
                index = str(int(index)-1)               
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def down(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != tk.END:                       
                self.lb.selection_clear(first=index)
                index = str(int(index)+1)       
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def comparison(self):
        pattern = re.compile('.*' + self.var.get() + '.*')
        return [w for w in self.lista if re.match(pattern, w)]