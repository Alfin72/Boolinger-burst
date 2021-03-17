
# -*- coding: utf-8 -*-
"""
"""
from kiteconnect import KiteConnect
import os
from datetime import datetime as dt
import pandas as pd
import numpy as np
import datetime
from csv import writer

location = ("D:\Test")
cwd = os.chdir(location)
Upper_Minute ="30minute"

# generate trading session
access_token = open("access_token.txt", 'r').read()
key_secret = open("api_key.txt", 'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)

# get dump of all NSE instruments
instrument_dump = kite.instruments("NSE")
instrument_df = pd.DataFrame(instrument_dump)

def data_downloader(name, interval, delta):
    token = kite.ltp('NSE:' + name)['NSE:' + name]['instrument_token']
    to_date = datetime.datetime.now().date()
    from_date = to_date - datetime.timedelta(days=delta)
    data = kite.historical_data(instrument_token=token, from_date=from_date, to_date=to_date, interval=interval,
                                continuous=False, oi=False)
    df = pd.DataFrame(data)
    D_C = df.iloc[:,[0,4]]
    D_C = D_C.set_index('date')
    # print(D_C)
    D_C['MA20'] = D_C['close'].rolling(window=20).mean()
    D_C['20dSTD'] = D_C['close'].rolling(window=20).std()

    D_C['Upper'] = D_C['MA20'] + (D_C['20dSTD'] * 2)
    D_C['Lower'] = D_C['MA20'] - (D_C['20dSTD'] * 2)
    # print(D_C['Upper'])
    # print(D_C['Lower'])
    # print(D_C[['close','MA20','Upper','Lower']])
    # print(D_C.tail(20))
    U_L = D_C.iloc[:,[3,4]]
    count = 3
    #print(U_L.tail(20))
    up = []
    low = []
    avg_up = []
    avg_low = []


    for i in U_L['Upper'].tail(count):
        up.append(round(i, 2))

    for i in U_L['Lower'].tail(count):
        low.append(round(i, 2))
    #print(up,low)

    for i in U_L['Upper'].tail(20):
        avg_up.append(i)
    for i in U_L['Lower'].tail(20):
        avg_low.append(i)
    fin_avg_up = sum(avg_up) / len(avg_up)
    fin_avg_low = sum(avg_low) / len(avg_low)
    #print(fin_avg_up,fin_avg_low,up[-1],low[-1])
    add_up_avg = fin_avg_up*1.5 / 100
    add_low_avg = fin_avg_low*1.5 / 100
    fin_avg_up = add_up_avg + fin_avg_up
    fin_avg_low = add_low_avg - fin_avg_low
    #print(fin_avg_up,fin_avg_low,up[-1],low[-1])

    if (((all(i < j for i, j in zip(up, up[1:]))) or (all(i == j for i, j in zip(up, up[1:])))) and (all(i > j for i, j in zip(low, low[1:])) or ((all(i == j for i, j in zip(low, low[1:])))))):
        if (up[-1] > fin_avg_up) or (low[-1] < fin_avg_low):
            print("Bollinger Burst in ", name)
            return "Bollinger Burst"
        else:
            print("No Bollinger Burst in ", name)
            return "No Bollinger Burst"

    else:
        print("No Bollinger Burst in ", name)
        return "No Bollinger Burst"

def bollinger_lists(share_list, time_list):
    result_list = []
    for i in share_list:
        for j in time_list:
            result = data_downloader(i, j, 100)#bollinger(i, j, 30, 3)
            now = dt.now()
            current_time = now.strftime("%H:%M:%S")
            result_list.append([i, j, result, current_time])

    for i in result_list:
        with open('bollinger burst.csv', 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(i)
            f_object.close()

#share_list = ['HINDCOPPER', 'TATAPOWER']
share_list =["ACC","ADANIENT","ADANIPORTS","AMARAJABAT","AMBUJACEM","APOLLOHOSP","APOLLOTYRE","ASHOKLEY","ASIANPAINT","AUROPHARMA","AXISBANK","BAJAJ-AUTO","BAJFINANCE","BAJAJFINSV","BALKRISIND","BANDHANBNK","BANKBARODA","BATAINDIA","BERGEPAINT","BEL","BHARATFORG","BPCL","BHARTIARTL","BHEL","BIOCON","BOSCHLTD","BRITANNIA","CADILAHC","CANBK","CENTURYTEX","CHOLAFIN","CIPLA","COALINDIA","COLPAL","CONCOR","CUMMINSIND","DABUR","DIVISLAB","DLF","DRREDDY","EICHERMOT","EQUITAS","ESCORTS","EXIDEIND","FEDERALBNK","GAIL","GLENMARK","GMRINFRA","GODREJCP","GODREJPROP","GRASIM","HAVELLS","HCLTECH","HDFCBANK","HDFC","HDFCLIFE","HEROMOTOCO","HINDALCO","HINDPETRO","HINDUNILVR","ICICIBANK","ICICIPRULI","NAUKRI","IDEA","IDFCFIRSTB","IBULHSGFIN","IOC","IGL","INDUSINDBK","INFY","INDIGO","ITC","JINDALSTEL","JSWSTEEL","JUBLFOOD","JUSTDIAL","KOTAKBANK","L&TFH","LT","LICHSGFIN","LUPIN","M&MFIN","MGL","M&M","MANAPPURAM","MARICO","MARUTI","MFSL","MINDTREE","MOTHERSUMI","MRF","MUTHOOTFIN","NATIONALUM","NCC","NESTLEIND","COFORGE","NMDC","NTPC","ONGC","PAGEIND","PETRONET","PIDILITIND","PEL","PFC","POWERGRID","PNB","PVR","RBLBANK","RELIANCE","RECLTD","SHREECEM","SRTRANSFIN","SIEMENS","SRF","SBIN","SBILIFE","SAIL","SUNPHARMA","SUNTV","TATACHEM","TCS","TATACONSUM","TATAMOTORS","TATAPOWER","TATASTEEL","TECHM","RAMCOCEM","TITAN","TORNTPHARM","TORNTPOWER","TVSMOTOR","UJJIVAN","ULTRACEMCO","UBL","MCDOWELL-N","UPL","VEDL","VOLTAS","WIPRO","ZEEL","NIFTY 50","NIFTY BANK"]
#interval = ['5minute', '30minute']
interval = ['day']
#data_downloader(share_list, "5minute", 100)
bollinger_lists(share_list, interval)