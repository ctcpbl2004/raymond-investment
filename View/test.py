# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 22:12:27 2018

@author: Raymond
"""

import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import date

root = tk.Tk()
# change ttk theme to 'clam' to fix issue with downarrow button
style = ttk.Style(root)
style.theme_use('clam')

class MyDateEntry(DateEntry):
    def __init__(self, master=None, **kw):
        DateEntry.__init__(self, master=None, **kw)
        # add black border around drop-down calendar
        self._top_cal.configure(bg='black', bd=1)
        # add label displaying today's date below
        tk.Label(self._top_cal, bg='gray90', anchor='w',
                 text='Today: %s' % date.today().strftime('%x')).pack(fill='x')

# create the entry and configure the calendar colors
de = MyDateEntry(root, year=2016, month=9, day=6,
                 selectbackground='gray80',
                 selectforeground='black',
                 normalbackground='white',
                 normalforeground='black',
                 background='gray90',
                 foreground='black',
                 bordercolor='gray90',
                 othermonthforeground='gray50',
                 othermonthbackground='white',
                 othermonthweforeground='gray50',
                 othermonthwebackground='white',
                 weekendbackground='white',
                 weekendforeground='black',
                 headersbackground='white',
                 headersforeground='gray70')
de.pack()
root.mainloop()



