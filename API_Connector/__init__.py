import quandl
import pandas as pd
import sys
import fix_yahoo_finance as yf

_QuandlAPI_token = 'fk-V2wGNzxxAiNnekenK'
quandl.ApiConfig.api_key = _QuandlAPI_token

def Get_Data(Quandl_Code,Start = None,End = None):
    if (Start == None) & (End == None):
        data = quandl.get(Quandl_Code)
    elif Start == None:
        data = quandl.get(Quandl_Code,end_date = End)
    elif End == None:
        data = quandl.get(Quandl_Code,start_date = Start)
    else:
        sys.stderr.write("ERROR!!")
    
    return data

def Get_Yahoo_Finance_data(Ticker, Start = None):
    
    if Start == None:
        Start = '1980-01-01'
    
    data = yf.download(Ticker,start = Start, progress = False)
    return data
    
    
    







