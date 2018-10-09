import DB_Connector
import API_Connector
import datetime
import pandas as pd
import time
import sys

class CreateData(object):
    @staticmethod
    def Create_FuturesData(Ticker):
        data = API_Connector.Get_Data(Ticker)
        data = data.drop(['Last','Change'],axis = 1)
        data = data.rename(columns = {'Previous Day Open Interest':'OI'})
        
        DB_Connector.InsertData.Futures(Ticker,data)
            
    @staticmethod
    def Create_EquityData(Ticker):
        pass
    
    @staticmethod
    def Create_MacroData(Ticker):
        data = API_Connector.Get_Data(Ticker)
        
        DB_Connector.InsertData.Macro(Ticker,data)

class Create_AllData(object):
    @staticmethod
    def Create_CHRIS():
        metadata = DB_Connector.Metadata.Get_CHRIS()
        Ticker_list = metadata['code'].tolist()
        
        n = 1
        for Ticker in Ticker_list:
            try:
                CreateData.Create_FuturesData('CHRIS/' + Ticker)
                #print("Progress = " + str(round(n/4074,4)*100) + '%, ' + str(Ticker))
                print(round(n/4074,4)*100.)
                time.sleep(1)
                n = n + 1
            except:
                sys.stderr.write("Error in " + Ticker + '.\n')





class UpdateData(object):
    def __init__(self):
        self.Summary_table = DB_Connector.GetData.Summary_table()
        self.Ticker_list = self.Summary_table['Ticker'].tolist()    
        self.Today = datetime.datetime.now()
        self.Today_Minus_30 = self.Today - datetime.timedelta(days = 30)
        self.Today_Minus_360 = self.Today - datetime.timedelta(days = 360)
        
    def Update_All(self):
        self.Update_EquityData()
        self.Update_FuturesData()
        self.Update_MacroData()
        
    def Update_EquityData(self):
        Equity_list = self.Summary_table[self.Summary_table['Category'] == 'Equity']['Ticker'].tolist()
        
        for Ticker in Equity_list:
            data = API_Connector.Get_Data(Ticker,Start = self.Today_Minus_30.strftime('%Y-%m-%d'))
            
            DB_Connector.InsertData.Equity(Ticker,data)
        
    def Update_FuturesData(self):
        Futures_list = self.Summary_table[self.Summary_table['Category'] == 'Futures']['Ticker'].tolist()
        
        for Ticker in Futures_list:
            data = API_Connector.Get_Data(Ticker,Start = self.Today_Minus_30.strftime('%Y-%m-%d'))
            data = data.drop(['Last','Change'],axis = 1)
            data = data.rename(columns = {'Previous Day Open Interest':'OI'})
            
            DB_Connector.InsertData.Futures(Ticker,data)

    def Update_MacroData(self):
        Macro_list = self.Summary_table[self.Summary_table['Category'] == 'Macro']['Ticker'].tolist()
        
        for Ticker in Macro_list:
            data = API_Connector.Get_Data(Ticker,Start = self.Today_Minus_360.strftime('%Y-%m-%d'))
            
            DB_Connector.InsertData.Macro(Ticker,data)



def Summarize_Data():
    DB_Connector.SummaryData.Equity()
    DB_Connector.SummaryData.Futures()
    DB_Connector.SummaryData.Macro()



