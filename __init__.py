# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 22:26:13 2018

@author: Raymond
"""

import DB_Connector
import API_Connector
import Controller
from Model import PortfolioAnalysis

import fix_yahoo_finance as yf
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


'''
data = DB_Connector.GetData.Multi_Equity(['SPY','VTI','AGG','GLD','USO'],Start = '2010-01-01')
print(data)

'''
Asset_Allocation = PortfolioAnalysis.Backtest_Asset_Allocation(['SPY','VTI','QQQ','VNQ','EEM','PFF','AGG','TLT','SHY','GLD','USO'])
Asset_Allocation.plot_correlation()

'''
Compare = PortfolioAnalysis.Relative_CumulativeReturn(['SPY','VTI','QQQ','VNQ','EEM','PFF','AGG','TLT','SHY','GLD','USO'],Start = '2018-01-01')
Compare.plot()




Summary_table = DB_Connector.GetData.Summary_table()
Tickers = Summary_table['Ticker'].tolist()

RiskReward = PortfolioAnalysis.RiskReward_Analyzer(Tickers,Start = '2018-01-01')
result = RiskReward.Generate_results()
print (result)
'''
'''
    def Balance_Portfolio(self,Weight):
        df = pd.DataFrame()
        df['Equity'] = Database_Functions.Fetch('MXWO Index')['MXWO Index']
        df['Bond'] = Database_Functions.Fetch('LBUSTRUU Index')['LBUSTRUU Index']
        df = df.dropna()
        df = df[df.index > '1989-02-01']
        #df = df
        Return_df = df.pct_change()

        Initial_amount = 1000000
        Equity_amount = Initial_amount * Weight[0]
        Bond_amount = Initial_amount * Weight[1]
        #print Weight[0],Weight[1]

        Shares_df = (Initial_amount / df).resample('M', how='last')
        Shares_df['Equity'] = Shares_df['Equity'] * Weight[0]
        Shares_df['Bond'] = Shares_df['Bond'] * Weight[1]
        Shares_df = Shares_df.resample('D', how='last').fillna(method='ffill')
        Amount_df = (Shares_df * df).dropna()
        Amount_df['Sum'] = Amount_df.sum(axis=1)

        Weight_df = pd.DataFrame()
        Weight_df['Equity'] = Amount_df['Equity'] / Amount_df['Sum']
        Weight_df['Bond'] = Amount_df['Bond'] / Amount_df['Sum']
        Portfolio_EC = (Weight_df * Return_df).sum(axis=1).cumsum().apply(np.exp)

        return Portfolio_EC

'''




