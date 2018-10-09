import quandl
import pandas as pd

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
        print("ERROR!!")
    
    return data

def Metadata_Wiki():
    metadata = pd.read_csv('https://www.quandl.com/api/v3/databases/CHRIS/metadata?api_key=fk-V2wGNzxxAiNnekenK')














