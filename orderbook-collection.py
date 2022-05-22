#! /usr/bin/env python

import datetime
import json
import csv
import os
import time
import pandas as pd
import requests
import sys

while(1):


    book = {}
    response = requests.get('https://api.bithumb.com/public/orderbook/BTC_KRW/?count=5')
    book = response.json()

    data = book['data']

    bids = (pd.DataFrame(data['bids'])).apply(pd.to_numeric,errors='ignore')

    bids.sort_values('price', ascending=False, inplace=True)
    bids = bids.reset_index(); del bids['index']
    bids['type'] = 0

    asks = (pd.DataFrame(data['asks'])).apply(pd.to_numeric,errors='ignore')

    asks.sort_values('price', ascending=True, inplace=True)
    asks['type'] = 1
    
    df = bids.append(asks)
    df['timestamp'] = datetime.datetime.now()
    
    timestamp = datetime.datetime.now()
    fn = timestamp.strftime("%Y-%m-%d") + '-bithumb-btc-orderbook' + '.csv'

    header = os.path.exists(fn)
    if header == False:
        df.to_csv(fn, index=False, header=True, mode = 'a')
    else:
        df.to_csv(fn, index=False, header=False, mode = 'a')
    
    time.sleep(1)

