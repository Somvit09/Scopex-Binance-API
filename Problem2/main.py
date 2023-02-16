import requests
import os
import binance
import pandas as pd
import plotly.graph_objects as go


endpoint = 'https://api.binance.us/api/v3/klines?symbol=LTCBTC&interval=1m'

response = requests.get(endpoint)



api_key = os.getenv('api_key')
api_secret = os.getenv('api_secret')

client = binance.Client(api_key=api_key, api_secret=api_secret)
coins = ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'BNBUSDT', 'DOTUSDT', 'LTCUSDT', 'XRPUSDT', 'LINKUSDT', 'UNIUSDT', 'DOGEUSDT']
dfs = []

for coin in coins:
    klines = client._klines(symbol=coin, interval=binance.Client.KLINE_INTERVAL_1MINUTE, limit=2880)
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df = df[['timestamp', 'open', 'high', 'low', 'close']]
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df.index.name = 'time'
    df.columns = [coin+'_'+col.lower() for col in df.columns]
    dfs.append(df)
for df in dfs:
    fig = go.Figure(data=[go.Candlestick(x=df.index, open=df[df.columns[0]], high=df[df.columns[1]], low=df[df.columns[2]], close=df[df.columns[3]])])
    fig.update_layout(title=df.columns[0][:-5]+' Candlestick Chart')
    fig.show()

