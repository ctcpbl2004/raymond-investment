# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 22:26:13 2018

@author: Raymond
"""

import DB_Connector
import API_Connector
import Controller
from Model import PortfolioAnalysis
from Model import FinancialEngineering
from View import StockViewer

import fix_yahoo_finance as yf
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np





app = StockViewer.MainWindow()


