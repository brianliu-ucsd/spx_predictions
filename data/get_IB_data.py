# This file contains the structure for receiving data from Interactive Brokers and using it to
# predict future prices using our ML model.

from ib_insync import *
from IPython.display import display
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
from datetime import *

def get_IB_data():

    # Ensure TWS has appropriate settings to accept API requests and that TWS app is running
    ib = IB()

    # This program runs on a remote server, while TWS must run on a localhost. 
    # Create a ssh tunnel between the two in order for connection to work.
    # Run this on local terminal: 
    # $ ssh -R 7497:localhost:7497 relaymile@76.185.2.134 -q -C -N

    ib.connect('127.0.0.1', 7497, clientId=1)

    # Setting requested data type to delayed + frozen (since we're on demo acct for now)
    # Documentation: https://interactivebrokers.github.io/tws-api/market_data_type.html
    ib.reqMarketDataType(4)

    # Getting contract details - the ML model is set up for predicting SPY
    contract = Index(symbol='SPX', exchange='CBOE')

    # Getting bar data
    # Historical data limitations: https://interactivebrokers.github.io/tws-api/historical_limitations.html
    # Historical data documentation: https://interactivebrokers.github.io/tws-api/historical_bars.html

    # Using current time to get recent data - note that times are interpreted as Eastern Time.
    now = datetime.now()
    date_time = now.strftime('%Y%m%d %H:%M:%S')
    date_time = '20230908 12:00:00'

    # Requesting data from last 60 seconds
    bars = ib.reqHistoricalData(
            contract,
            endDateTime=date_time,
            durationStr='60 S',
            barSizeSetting='1 secs',
            whatToShow='TRADES',
            useRTH=True,
            formatDate=1,
            keepUpToDate=False,
    )

    df = util.df(bars)
    
    # Drop unneeded columns - average, barCount
    df = df.drop(columns=['average', 'barCount'])

    # Rename columns to model format
    new_cols = ['Date', 'Open', 'High', 'Low', 'Last', 'Volume']
    df.columns = new_cols

    # Add the following columns - NumberOfTrades, bidVolume, askVolume, speed, acceleration, distance, and VWAP
    df['NumberOfTrades'] = 0
    df['BidVolume'] = 0
    df['AskVolume'] = 0
    df['Speed'] = df['Last'].diff() / df['Date'].diff().dt.total_seconds()   
    df['Acceleration'] = df['Speed'].diff() / df['Date'].diff().dt.total_seconds()
    df['Distance'] = df['Last'].diff().cumsum()
    df['VWAP'] = (df['Last'] * df['Volume']).cumsum() / df['Volume'].cumsum()
    
    # Drop date
    df = df.drop(columns=['Date'])

    # Filter out NaN and inf values (MinMaxScaler can't handle)
    df = df.fillna(0)
    df = df.replace(np.inf, 9999)
    df = df.replace(-np.inf, -9999)

    # Convert data into numpy array - use float32 to save memory
    dataset = df.values.astype('float32')

    # Normalize dataset values
    sc = MinMaxScaler(feature_range=(0,1))
    dataset = sc.fit_transform(dataset)

    # Reshape to fit model
    dataset = np.reshape(dataset, (dataset.shape[1], dataset.shape[0], 1))

    # Import model
    model = load_model('./model/v1_model.h5')

    # Make predictions
    predicted_prices = model.predict(dataset)
    predicted_prices = sc.inverse_transform(predicted_prices)

    # Convert to readable df
    cols = ['Open', 'High', 'Low', 'Last', 'Volume', 'NumberOfTrades', 'BidVolume', 'AskVolume', 'Speed', 'Acceleration', 'Distance', 'VWAP']
    result = pd.DataFrame(predicted_prices, columns=cols)
    display(result)

    # Compare to actual:
    predict_time = '20230908 12:02:00'

    # Requesting data from prediction timeframe
    bars = ib.reqHistoricalData(
            contract,
            endDateTime=predict_time,
            durationStr='60 S',
            barSizeSetting='1 secs',
            whatToShow='TRADES',
            useRTH=True,
            formatDate=1,
            keepUpToDate=False,
    )

    df = util.df(bars)
    df = df.head(12)
    
    # Drop unneeded columns - average, barCount
    df = df.drop(columns=['average', 'barCount'])

    # Rename columns to model format
    new_cols = ['Date', 'Open', 'High', 'Low', 'Last', 'Volume']
    df.columns = new_cols

    # Add the following columns - NumberOfTrades, bidVolume, askVolume, speed, acceleration, distance, and VWAP
    df['NumberOfTrades'] = 0
    df['BidVolume'] = 0
    df['AskVolume'] = 0
    df['Speed'] = df['Last'].diff() / df['Date'].diff().dt.total_seconds()   
    df['Acceleration'] = df['Speed'].diff() / df['Date'].diff().dt.total_seconds()
    df['Distance'] = df['Last'].diff().cumsum()
    df['VWAP'] = (df['Last'] * df['Volume']).cumsum() / df['Volume'].cumsum()
    
    # Drop date
    df = df.drop(columns=['Date'])

    display(df)

if __name__ == '__main__':
    get_IB_data()