# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 19:56:51 2018

@author: Raymond
"""
import numpy as np
from scipy import stats
import sys
import random
import pandas as pd

class Monte_Carlo():
    @staticmethod
    def Simulate_StockPrice(Time, Paths, mu, Std, dt):
        S = np.zeros((Time, Paths))
        S[0] = 100
        
        for t in range(1, Time):
            S[t] = S[t - 1] * np.exp((mu - 0.5 *Std**2)*dt + Std*np.sqrt(dt)*np.random.standard_normal(Paths))
        
        df = pd.DataFrame(S)
        return df
        

def Black_Scholes(S,K,t,r,Sigma,CallPut_Flag):
    
    S = float(S)
    K = float(K)
    t = float(t) / 252.
    r = float(r)
    Sigma = float(Sigma)
    
    d1 =( np.log(S/K) + (r + 0.2 * Sigma ** 2) * t) / (Sigma * np.sqrt(t))
    d2 = d1 - Sigma * np.sqrt(t)
    
    Nd1 = stats.norm.cdf(d1)
    Nd2 = stats.norm.cdf(d2)
    
    Call = S * np.exp(-r * t) * Nd1 - K * np.exp(-r * t) * Nd2
    Put = S * np.exp(-r*t) * (Nd1 - 1.) - K * np.exp(-r*t) * (Nd2 - 1)
    
    if CallPut_Flag == 'Call' or 'call' or 'C' or 'c':
        return Call
    elif CallPut_Flag == 'Put' or 'put' or 'P' or 'p':
        return Put
    else:
        sys.stderr.write("Error in CallPut_Flag. \n")

def Delta(S,K,t,r,Sigma,CallPut_Flag):
    S = float(S)
    K = float(K)
    t = float(t) / 252.
    r = float(r)
    Sigma = float(Sigma)
    
    d1 =( np.log(S/K) + (r + 0.2 * Sigma ** 2) * t) / (Sigma * np.sqrt(t))
    
    Nd1 = stats.norm.cdf(d1)
    
    if CallPut_Flag == 'Call' or 'call' or 'C' or 'c':
        return Nd1
    elif CallPut_Flag == 'Put' or 'put' or 'P' or 'p':
        return Nd1 - 1.
    else:
        sys.stderr.write("Error in CallPut_Flag. \n")
    

def Implied_Volatility(S,K,t,r,Premium,CallPut_Flag):
    
    accuracy = 0.00001
    Low_bound = 0.
    Up_bound = 2.
    
    if CallPut_Flag == 'Call' or 'call' or 'C' or 'c':
        
        if (Black_Scholes(S,K,t,r,Low_bound,'Call') - Premium) * (Black_Scholes(S,K,t,r,Up_bound,'Call') - Premium) < 0.:
    
            while (Up_bound - Low_bound)/2. >= accuracy:
                Mid = (Low_bound + Up_bound)/2.
                if (Black_Scholes(S,K,t,r,Mid,'Call') - Premium) * (Black_Scholes(S,K,t,r,Low_bound,'Call') - Premium) < 0.:
                    Up_bound = Mid
                    
                elif (Black_Scholes(S,K,t,r,Mid,'Call') - Premium) * (Black_Scholes(S,K,t,r,Up_bound,'Call') - Premium) < 0.:
                    Low_bound = Mid
                else:
                    Up_bound = Mid
                    Low_bound = Mid
    
            
            ImpVol = (Low_bound + Up_bound)/2.
            return ImpVol
        else:
            raise Exception('Error!Please choose a interval where the Error change its signs')
    
    elif CallPut_Flag == 'Put' or 'put' or 'P' or 'p':

        if (Black_Scholes(S,K,t,r,Low_bound,'Put') - Premium) * (Black_Scholes(S,K,t,r,Up_bound,'Put') - Premium) < 0.:
    
            while (Up_bound - Low_bound)/2. >= accuracy:
                Mid = (Low_bound + Up_bound)/2.
                if (Black_Scholes(S,K,t,r,Mid,'Put') - Premium) * (Black_Scholes(S,K,t,r,Low_bound,'Put') - Premium) < 0.:
                    Up_bound = Mid
                    
                elif (Black_Scholes(S,K,t,r,Mid,'Put') - Premium) * (Black_Scholes(S,K,t,r,Up_bound,'Put') - Premium) < 0.:
                    Low_bound = Mid
                else:
                    Up_bound = Mid
                    Low_bound = Mid
    
            
            ImpVol = (Low_bound + Up_bound)/2.
            return ImpVol
        else:
            raise Exception('Error!Please choose a interval where the Error change its signs')

    else:
        raise Exception("Error in CallPut_Flag. \n")
















