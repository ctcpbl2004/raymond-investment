import pandas as pd
import sqlite3
import sys

_db_path = 'Database\Database.db'

class GetData(object):
    @staticmethod    
    def Equity(Ticker, Start=None, End = None):
        connection = sqlite3.connect(_db_path)
        cursor = connection.cursor()
        
        if (Start == None) & (End == None):
            cursor.execute("SELECT Date, Open, High, Low, Close, Volume, Dividends, AdjClose FROM Equity WHERE Ticker = ?",(Ticker,))
        elif End == None:
            cursor.execute("SELECT Date, Open, High, Low, Close, Volume, Dividends, AdjClose FROM Equity WHERE Ticker = ? AND Date >= ?",(Ticker, Start))
        elif Start == None:
            cursor.execute("SELECT Date, Open, High, Low, Close, Volume, Dividends, AdjClose FROM Equity WHERE Ticker = ? AND Date <= ?",(Ticker, End))
        elif (Start != None) & (End != None):
            cursor.execute("SELECT Date, Open, High, Low, Close, Volume, Dividends, AdjClose FROM Equity WHERE Ticker = ? AND Date BETWEEN ? AND ?",(Ticker, Start, End))
        else:
            raise Exception("Error in getting data from db(Equity).")
    
        data = cursor.fetchall()
        
        connection.close()
        
        Date_list = []
        Open_list = []
        High_list = []
        Low_list = []
        Close_list = []
        Volume_list = []
        Dividends_list = []
        AdjClose_list = []
        
        for row in data:
            Date_list.append(row[0])
            Open_list.append(row[1])
            High_list.append(row[2])
            Low_list.append(row[3])
            Close_list.append(row[4])
            Volume_list.append(row[5])
            Dividends_list.append(row[6])
            AdjClose_list.append(row[7])
    
        df = pd.DataFrame(index = Date_list, columns = ["Open","High","Low","Close","Volume","Dividends","AdjClose"])
        df.index = pd.to_datetime(df.index)
        
        df['Open'] = Open_list
        df['High'] = High_list
        df['Low'] = Low_list
        df['Close'] = Close_list
        df['Volume'] = Volume_list
        df['Dividends'] = Dividends_list
        df['AdjClose'] = AdjClose_list
        
        df.sort_index()
        
        return df

    @staticmethod
    def Futures(Ticker, Start=None, End = None):
        connection = sqlite3.connect(_db_path)
        cursor = connection.cursor()
        
        if (Start == None) & (End == None):
            cursor.execute("SELECT Date, Open, High, Low, Settle, Volume, OI FROM Futures WHERE Ticker = ?",(Ticker,))
        elif End == None:
            cursor.execute("SELECT Date, Open, High, Low, Settle, Volume, OI FROM Futures WHERE Ticker = ? AND Date >= ?",(Ticker, Start))
        elif Start == None:
            cursor.execute("SELECT Date, Open, High, Low, Settle, Volume, OI FROM Futures WHERE Ticker = ? AND Date <= ?",(Ticker, End))
        elif (Start != None) & (End != None):
            cursor.execute("SELECT Date, Open, High, Low, Settle, Volume, OI FROM Futures WHERE Ticker = ? AND Date BETWEEN ? AND ?",(Ticker, Start, End))
        else:
            raise Exception("Error in getting data from db(Futures).")
    
        data = cursor.fetchall()
        connection.close()
        
        Date_list = []
        Open_list = []
        High_list = []
        Low_list = []
        Settle_list = []
        Volume_list = []
        OI_list = []
        
        for row in data:
            Date_list.append(row[0])
            Open_list.append(row[1])
            High_list.append(row[2])
            Low_list.append(row[3])
            Settle_list.append(row[4])
            Volume_list.append(row[5])
            OI_list.append(row[6])
    
        df = pd.DataFrame(index = Date_list, columns = ["Open","High","Low","Settle","Volume","OI"])
        df.index = pd.to_datetime(df.index)
        
        df['Open'] = Open_list
        df['High'] = High_list
        df['Low'] = Low_list
        df['Settle'] = Settle_list
        df['Volume'] = Volume_list
        df['OI'] = OI_list
        
        df.sort_index()
        
        return df


    @staticmethod
    def Macro(Ticker, Start=None, End = None):
        connection = sqlite3.connect(_db_path)
        cursor = connection.cursor()
        
        if (Start == None) & (End == None):
            cursor.execute("SELECT Date,Value FROM Futures WHERE Ticker = ?",(Ticker,))
        elif End == None:
            cursor.execute("SELECT Date,Value FROM Futures WHERE Ticker = ? AND Date >= ?",(Ticker, Start))
        elif Start == None:
            cursor.execute("SELECT Date,Value FROM Futures WHERE Ticker = ? AND Date <= ?",(Ticker, End))
        elif (Start != None) & (End != None):
            cursor.execute("SELECT Date,Value FROM Futures WHERE Ticker = ? AND Date BETWEEN ? AND ?",(Ticker, Start, End))
        else:
            raise Exception("Error in getting data from db(Macro).")
    
        data = cursor.fetchall()
        
        connection.close()
        
        Date_list = []
        Value_list = []
        
        for row in data:
            Date_list.append(row[0])
            Value_list.append(row[1])
    
        df = pd.DataFrame(index = Date_list, columns = ["Value"])
        df.index = pd.to_datetime(df.index)
        
        df['Value'] = Value_list
        
        df.sort_index()
        
        return df

    @staticmethod
    def Summary_table():
        connection = sqlite3.connect(_db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Summary_table")
        
        data = cursor.fetchall()
        
        connection.close()
        
        Category_list = []
        Ticker_list = []
        Start_list = []
        End_list = []
        Count_list = []
        
        for row in data:
            Category_list.append(row[0])
            Ticker_list.append(row[1])
            Start_list.append(row[2])
            End_list.append(row[3])
            Count_list.append(row[4])
        
        df = pd.DataFrame(index = range(len(Ticker_list)),columns = ['Category','Ticker','Start','End','Count'])
        
        df['Category'] = Category_list
        df['Ticker'] = Ticker_list
        df['Start'] = Start_list
        df['End'] = End_list
        df['Count'] = Count_list
        
        return df

class InsertData(object):
    @staticmethod
    def Equity(Ticker,df):
        connection = sqlite3.connect(_db_path)
        cursor = connection.cursor()
        
        NumberOfData = len(df)
        
        for i in range(NumberOfData):
            
            Date = str(df.index[i])[:10]
            Open = df['Open'][i]
            High = df['High'][i]
            Low = df['Low'][i]
            Close = df['Close'][i]
            Volume = df['Volume'][i]
            Dividends = df['Dividends'][i]
            AdjClose = df['AdjClose'][i]
            
            cursor.execute("INSERT OR REPLACE INTO Equity VALUES (?,?,?,?,?,?,?,?,?)",(Ticker,Date, Open, High, Low, Close, Volume, Dividends, AdjClose))        

        sys.stderr.write("[info] wrote %s rows to db. \n" % (len(df)))
        
        connection.commit()
        connection.close()
        
        sys.stderr.write("[info] %s data created successfully.\n" % (Ticker))

    @staticmethod
    def Futures(Ticker,df):
        connection = sqlite3.connect(_db_path)
        cursor = connection.cursor()
        
        NumberOfData = len(df)
        
        for i in range(NumberOfData):
            
            Date = str(df.index[i])[:10]
            Open = df['Open'][i]
            High = df['High'][i]
            Low = df['Low'][i]
            Settle = df['Settle'][i]
            Volume = df['Volume'][i]
            OI = df['OI'][i]
            
            cursor.execute("INSERT OR REPLACE INTO Futures VALUES (?,?,?,?,?,?,?,?)",(Ticker,Date, Open, High, Low, Settle, Volume, OI))        
            
        sys.stderr.write("[info] wrote %s rows to db. \n" % (len(df)))
        
        connection.commit()
        connection.close()
        
        sys.stderr.write("[info] %s data created successfully.\n" % (Ticker))

    @staticmethod
    def Macro(Ticker,df):
        connection = sqlite3.connect(_db_path)
        cursor = connection.cursor()
        
        NumberOfData = len(df)
        
        for i in range(NumberOfData):
            
            Date = str(df.index[i])[:10]
            Value = df['Value'][i]
            
            cursor.execute("INSERT OR REPLACE INTO Macro VALUES (?,?,?)",(Ticker,Date, Value))        
            
        sys.stderr.write("[info] wrote %s rows to db. \n" % (len(df)))
        
        connection.commit()
        connection.close()
        
        sys.stderr.write("[info] %s data created successfully.\n" % (Ticker))
        
class DeleteData(object):
    @staticmethod
    def Equity(Ticker):
        connection = sqlite3.connect(_db_path)
        cursor = connection.cursor()
        
        cursor.execute("DELETE FROM Equity WHERE Ticker = ?",(Ticker,))
        
        connection.commit()
        connection.close()

    @staticmethod
    def Futures(Ticker):
        connection = sqlite3.connect(_db_path)
        cursor = connection.cursor()
        
        cursor.execute("DELETE FROM Futures WHERE Ticker = ?",(Ticker,))
        
        connection.commit()
        connection.close()

    @staticmethod
    def Macro(Ticker):
        connection = sqlite3.connect(_db_path)
        cursor = connection.cursor()
        
        cursor.execute("DELETE FROM Macro WHERE Ticker = ?",(Ticker,))
        
        connection.commit()
        connection.close()

class SummaryData(object):
    @staticmethod
    def Equity():
        connection = sqlite3.connect(_db_path)
        cursor = connection.cursor()
        
        cursor.execute("SELECT Ticker, MIN(Date), MAX(Date), COUNT(Ticker) FROM Equity GROUP BY Ticker")        
        
        data = cursor.fetchall()
        
        for each in data:
            cursor.execute("INSERT OR REPLACE INTO Summary_table VALUES (?,?,?,?,?)",('Equity',each[0],each[1],each[2],each[3]))
        
        connection.commit()
        connection.close()

    @staticmethod
    def Futures():
        connection = sqlite3.connect(_db_path)
        cursor = connection.cursor()
        
        cursor.execute("SELECT Ticker, MIN(Date), MAX(Date), COUNT(Ticker) FROM Futures GROUP BY Ticker")        
        
        data = cursor.fetchall()
        
        for each in data:
            cursor.execute("INSERT OR REPLACE INTO Summary_table VALUES (?,?,?,?,?)",('Futures',each[0],each[1],each[2],each[3]))
        
        connection.commit()
        connection.close()

    @staticmethod
    def Macro():
        connection = sqlite3.connect(_db_path)
        cursor = connection.cursor()
        
        cursor.execute("SELECT Ticker, MIN(Date), MAX(Date), COUNT(Ticker) FROM Macro GROUP BY Ticker")        
        
        data = cursor.fetchall()
        
        for each in data:
            cursor.execute("INSERT OR REPLACE INTO Summary_table VALUES (?,?,?,?,?)",('Macro',each[0],each[1],each[2],each[3]))
        
        connection.commit()
        connection.close()

class Metadata(object):
    @staticmethod
    def Insert_FRED():
        path = 'metadata/FRED_metadata.csv'
        data = pd.read_csv(path)
        
        connection = sqlite3.connect(_db_path)
        cursor = connection.cursor()
        
        
        for i in range(len(data)):
            cursor.execute("INSERT INTO FRED_metadata VALUES (?,?,?,?,?,?)",(data.ix[i][0],data.ix[i][1],data.ix[i][2],data.ix[i][3],data.ix[i][4],data.ix[i][5]))
        
        connection.commit()
        connection.close()
        
    @staticmethod
    def Insert_CHRIS():
        path = 'metadata/CHRIS_metadata.csv'
        data = pd.read_csv(path)
        
        connection = sqlite3.connect(_db_path)
        cursor = connection.cursor()
        
        for i in range(len(data)):
            cursor.execute("INSERT INTO CHRIS_metadata VALUES (?,?,?,?,?,?)",(data.ix[i][0],data.ix[i][1],data.ix[i][2],data.ix[i][3],data.ix[i][4],data.ix[i][5]))
        
        connection.commit()
        connection.close()

    @staticmethod
    def Get_FRED():
        connection = sqlite3.connect(_db_path)
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM FRED_metadata")
        
        data = cursor.fetchall()
        
        code_list = []
        name_list = []
        description_list = []
        refreshed_at_list = []
        from_date_list = []
        to_date_list = []
        
        for each in data:
            code_list.append(each[0])
            name_list.append(each[1])
            description_list.append(each[2])
            refreshed_at_list.append(each[3])
            from_date_list.append(each[4])
            to_date_list.append(each[5])
                
        df = pd.DataFrame(columns = ['code','name','description','refreshed_at','from_date','to_date'])
        df['code'] = code_list
        df['name'] = name_list
        df['description'] = description_list
        df['refreshed_at'] = refreshed_at_list
        df['from_date'] = from_date_list
        df['to_date'] = to_date_list
        
        return df

    @staticmethod
    def Get_CHRIS():
        connection = sqlite3.connect(_db_path)
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM CHRIS_metadata")
        
        data = cursor.fetchall()
        
        code_list = []
        name_list = []
        description_list = []
        refreshed_at_list = []
        from_date_list = []
        to_date_list = []
        
        for each in data:
            code_list.append(each[0])
            name_list.append(each[1])
            description_list.append(each[2])
            refreshed_at_list.append(each[3])
            from_date_list.append(each[4])
            to_date_list.append(each[5])
                
        df = pd.DataFrame(columns = ['code','name','description','refreshed_at','from_date','to_date'])
        df['code'] = code_list
        df['name'] = name_list
        df['description'] = description_list
        df['refreshed_at'] = refreshed_at_list
        df['from_date'] = from_date_list
        df['to_date'] = to_date_list
        
        return df





