import MetaTrader5 as mt5
import pandas as pd
from pandas import DataFrame 
import numpy as np
from datetime import datetime

class MT5:

    def __init__(self):
        if not mt5.initialize():
            print("initialize() failed")
            mt5.shutdown()
 
    def get_ticks(self, symbol:str, from_date:datetime, to_date:datetime)->DataFrame:
 
        ticks = mt5.copy_ticks_range(symbol,  
                                     datetime.strptime(from_date, '%Y-%m-%d %H:%M:%S.%f'), 
                                     datetime.strptime(to_date, '%Y-%m-%d %H:%M:%S.%f'),  
                                     mt5.COPY_TICKS_ALL)

        # Transform Tuple into a DataFrame
        df_ticks = pd.DataFrame(ticks)

        # Convert number format of the date into date format
        df_ticks["time"] = pd.to_datetime(df_ticks["time"], unit="s").astype(str)

        # df_ticks = df_ticks.set_index("time")
        df_ticks.rename(columns={'time': 'timestamp'}, inplace=True)

        return df_ticks[['timestamp', 'bid', 'ask']]
    
    def get_rates(self, symbol:str, from_date:datetime, to_date:datetime, timeframe:str)->DataFrame:
        # Extract ohlc 
        rates = mt5.copy_rates_range(symbol, self.__match_timeframe(timeframe), 
                            datetime.strptime(from_date, '%Y-%m-%d %H:%M:%S.%f'), 
                            datetime.strptime(to_date, '%Y-%m-%d %H:%M:%S.%f'))

        # Transform Tuple into a DataFrame
        df_rates = pd.DataFrame(rates)
        #df_rates['time'] = df_rates['time'] + 16200
        # Convert number format of the date into date format
        df_rates["time"] = pd.to_datetime(df_rates["time"], unit="s").astype(str)

        # df_rates = df_rates.set_index("time")
        df_rates.rename(columns={'time': 'timestamp'}, inplace=True)

        return df_rates[['timestamp', 'open', 'high', 'low',	'close']]
    
    def __match_timeframe(self, timeframe):
        if timeframe == 'M1':
                return mt5.TIMEFRAME_M1
        elif timeframe == 'M2':
                return mt5.TIMEFRAME_M2
        elif timeframe == 'M3':
                return mt5.TIMEFRAME_M3
        elif timeframe == 'M4':
                return mt5.TIMEFRAME_M4
        elif timeframe == 'M5':
                return mt5.TIMEFRAME_M5
        elif timeframe == 'M6':
                return mt5.TIMEFRAME_M6
        elif timeframe == 'M10':
                return mt5.TIMEFRAME_M10
        elif timeframe == 'M15':
                return mt5.TIMEFRAME_M15
        elif timeframe == 'M20':
                return mt5.TIMEFRAME_M20
        elif timeframe == 'M30':
                return mt5.TIMEFRAME_M30
        elif timeframe == 'H1':
                return mt5.TIMEFRAME_H1
        elif timeframe == 'H2':
                return mt5.TIMEFRAME_H2
        elif timeframe == 'H3':
                return mt5.TIMEFRAME_H3
        elif timeframe == 'H4':
                return mt5.TIMEFRAME_H4
        elif timeframe == 'H6':
                return mt5.TIMEFRAME_H6
        elif timeframe == 'H8':
                return mt5.TIMEFRAME_H8
        elif timeframe == 'H12':
                return mt5.TIMEFRAME_H12
        elif timeframe == 'D1':
                return mt5.TIMEFRAME_D1
        elif timeframe == 'W1':
                return mt5.TIMEFRAME_W1
        elif timeframe == 'MN1':
                return mt5.TIMEFRAME_MN1
        else:
                return mt5.TIMEFRAME_D1
            
#########################################################
from typing import Union
from fastapi import FastAPI, Body
import json
app = FastAPI()


@app.post("/get_rates/")
async def get_rates(param: dict = Body(
        example={
            "symbol": "EURUSD", 
            "from_date": "2022-04-13 09:00:00.037761", 
            "to_date": "2022-04-14 09:00:00.037761", 
            "timeframe": "M15"
        },
    )):
    mtt = MT5()
    df = mtt.get_rates(param['symbol'],
    param['from_date'],
    param['to_date'],
    param['timeframe'])
    return df.to_dict(orient='records')

@app.post("/get_ticks/")
async def get_ticks(param: dict= Body(
        example={
            "symbol": "EURUSD", 
            "from_date": "2022-04-14 09:00:00.037761", 
            "to_date": "2022-04-14 09:05:00.037761" 
        },
    )):
    mtt = MT5()
    df = mtt.get_ticks(param['symbol'],
    param['from_date'],
    param['to_date'])
    
    return df.to_dict(orient='records')


