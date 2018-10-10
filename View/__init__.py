import tkinter as tk
from tkinter import ttk

class MainWindow(tk.Tk):
    def __init__(self):
        self.root = tk.Tk()
        self.root.wm_title('Dashboard')
        self.root.geometry('1800x1000')
        self.root.resizable(False, False)
        
        self.root.mainloop()



