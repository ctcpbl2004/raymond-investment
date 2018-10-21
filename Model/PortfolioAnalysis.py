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
        
        
def Evaluate_Performance(df):
    if len(df.columns) == 1:
        days = df.index[-1] - df.index[0]
        years = days.days/365.
        Annual_Return = df[df.columns[0]][-1] ** (1/years) - 1.

        df_pctchg = df.pct_change()
        Annual_Volatility = np.std(df_pctchg[df_pctchg.columns[0]])*np.sqrt(252)
        
        Sharpe_Ratio = Annual_Return / Annual_Volatility
        
        df['New_High'] = df[df.columns[0]].cummax()
        df['Drawdown'] = df[df.columns[0]] - df['New_High']
        MaxDrawDown = min(df['Drawdown'])
        
        Performance = pd.DataFrame(index = ['Annual Return','Annual Volatility','Sharpe Ratio','Max Drawdown'], columns = ['Custom Portfolio'])
        Performance['Custom Portfolio'] = [Annual_Return,Annual_Volatility,Sharpe_Ratio,MaxDrawDown]
        
        return Performance
        
    else:
        pass        
        

    
    
    
class Relative_CumulativeReturn(object):
    def __init__(self, Tickers, Start):
        data = DB_Connector.GetData.Multi_Equity(Tickers, Start)
        self.return_df = data / data.ix[0] - 1
        
    def plot(self):
        self.return_df.plot()
    
    def output(self):
        return self.return_df


class Backtest(object):
    
    def __init__(self, holdings_dict, Rebalance_period, Start):
        
        self.data = DB_Connector.GetData.Multi_Equity(holdings_dict.keys(), Start)
        self.Rebalance_freq = Rebalance_period
        self.holdings_dict = holdings_dict
        
        if sum(self.holdings_dict.values()) != 1.:
            sys.stderr.write("Error in portfolio's weight. \n")
            return None
            
        
        
        
    def Result(self):
            
        Return_data = self.data.pct_change()
        
        Initial_Amount = 1000000
        
        Shares_data = (Initial_Amount/self.data).resample(self.Rebalance_freq).last()
        Shares_data = Shares_data.append(Initial_Amount/self.data.iloc[0]).sort_index()
        
        for each in self.holdings_dict:
            
            Shares_data[each] = Shares_data[each] * self.holdings_dict[each]
        
        Shares_data = Shares_data.resample('D').last().fillna(method='ffill')
        
        Amount_data = (Shares_data * self.data).dropna()
        
        Amount_data['Sum'] = Amount_data.sum(axis=1)
        
        Weight_data = pd.DataFrame(columns = self.holdings_dict.keys())
        
        for each in self.holdings_dict.keys():
            Weight_data[each] = Amount_data[each] / Amount_data['Sum']
        
        Weight_data['Sum'] = Weight_data.sum(axis = 1)
        
        Portfolio_EC = (Weight_data * Return_data).sum(axis=1).cumsum().apply(np.exp)
        Portfolio_EC.name = 'NAV'
        
        df = pd.DataFrame()
        df['NAV'] = Portfolio_EC
        df['NAV'].plot(legend = True,label = str(self.holdings_dict))

        
        Weight_df = pd.DataFrame(columns = ['Weight'], index = self.holdings_dict.keys())
        Weight_df['Weight'] = list(self.holdings_dict.values())
        
        print ("=============================")
        print (Weight_df)
        print (Evaluate_Performance(df))
        print ("=============================")

        return df

    def _generate_list(self,size,default_value):
        return_list = np.zeros((1,size)) + default_value
        return return_list


class Correlation_Anaysis(object):
    
    def __init__(self, Tickers, Start, End):
        self.data = DB_Connector.GetData.Multi_Equity(Tickers, Start)
    
    def Matrix(self):
        Return_data = self.data.pct_change()
        Correlation_matrix = Return_data.corr()
        
        return Correlation_matrix
    
    def Matrix_plot(self):
        Correlation_matrix = round(self.Matrix(),2)
        
        fig, ax = plt.subplots(figsize=(8,6))
        ax.imshow(Correlation_matrix.values, cmap='RdBu')
        
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

































