# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 11:03:33 2018

@author: Raymond
"""

import DB_Connector
import pandas as pd
import numpy as np
import sys
import matplotlib
import matplotlib.pyplot as plt

class Analyzer(object):
    
    def __init__(self, df):
        self.data = df
    
    def Return_Yearly(self):
        Yearly_data = self.data.resample('A').last()
        Yearly_data['Return'] = Yearly_data['AdjClose']/Yearly_data['AdjClose'].shift(1) - 1
        return Yearly_data['Return'].dropna()
    
    
    
class RiskReward_Analyzer(object):
    
    def __init__(self, Tickers_list, Start = None):
        
        self.Tickers_list = Tickers_list
        self.StartDate = Start
        
            
        
    def Get_Single_RiskReward(self, Ticker):
        data = DB_Connector.GetData.Equity(Ticker, Start = self.StartDate)
        data['Return'] = data['AdjClose'] / data['AdjClose'].shift(1) - 1
        
        Average_DailyReturn = np.mean(data['Return'].dropna())
        
        Annualized_Return = (( 1 + Average_DailyReturn) ** 252) - 1.
        Annualized_Volatility = np.std(data['Return'].dropna()) * (252 ** 0.5)
        
        return (Annualized_Return,Annualized_Volatility)
                
        
    def Generate_results(self):
        Return_list = []
        Volatility_list = []
        
        
        for Ticker in self.Tickers_list:
            profile = self.Get_Single_RiskReward(Ticker)
            Return_list.append(profile[0])
            Volatility_list.append(profile[1])
        
        df = pd.DataFrame(columns = ['Return','Volatility'], index = self.Tickers_list)
        df ['Return'] = Return_list
        df['Volatility'] = Volatility_list
        
        return df
    
    def scatter_plot(self):
        
        data = self.Generate_results()
        data.plot.scatter(x = 'Volatility', y = 'Return')
        
        
        
        
        

    
    
    
class Relative_CumulativeReturn(object):
    def __init__(self, Tickers, Start):
        data = DB_Connector.GetData.Multi_Equity(Tickers, Start)
        self.return_df = data / data.ix[0] - 1
        
    def plot(self):
        self.return_df.plot()
    
    def output(self):
        return self.return_df


class Backtest_Asset_Allocation(object):
    
    def __init__(self, Tickers, Weight = None, Rebalance_period = None):
        
        NumberOfComponent = len(Tickers)
        '''
        if Weight == 'Equal':
            Weight_list = self._generate_list(NumberOfComponent,1./NumberOfComponent)
            
        elif (type(Weight) == list) and (len(Weight) == len(Tickers)) and (sum(Weight) == 1.):
            Weight_list = Weight
        else:
            sys.stderr.write('[Error] Wrong input in "Weight" parameter. \n')
        
        if Rabalance_period in ('Buy&Hold','Daily','Monthly','Quarterly','Annual'):
            pass
        else:
            sys.stderr.write('[Error] Wrong input in "Rebalance_perild". \n')
        '''
        
        
        
        
        
        
        
        
        
        
        self.data = DB_Connector.GetData.Multi_Equity(Tickers)
        
        









    def _generate_list(self,size,default_value):
        return_list = np.zeros((1,size)) + default_value
        return return_list

    def Component_Correlation(self):
        
        Return_data = self.data.pct_change()
        Correlation_matrix = Return_data.corr()
        
        return Correlation_matrix

    def plot_correlation(self):
        
        Correlation_matrix = round(self.Component_Correlation(),2)
        
        fig, ax = plt.subplots(figsize=(8,6))
        im = ax.imshow(Correlation_matrix.values, cmap='RdBu')
        
        ax.set_xticks(np.arange(len(Correlation_matrix.columns)))
        ax.set_yticks(np.arange(len(Correlation_matrix.columns)))

        ax.set_xticklabels(Correlation_matrix.columns)
        ax.set_yticklabels(Correlation_matrix.columns)
        
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        
        
        for i in range(len(Correlation_matrix.columns)):
            for j in range(len(Correlation_matrix.columns)):
                ax.text(j, i, Correlation_matrix.values[i, j], ha="center", va="center", color="w")
        
        ax.set_title("Correlation matrix of multiple assets")
        fig.tight_layout()
        plt.show()































