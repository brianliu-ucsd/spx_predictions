import pandas as pd
from IPython.display import display
import time

# This is made for sierrachart data

start_time = time.time()

df = pd.read_csv('./storage/2022sierra_tick.csv')

# Calculate speed, acceleration, and distance
# Convert 'Time' to datetime format
df['Time'] = pd.to_datetime(df['Time'])
df['TimeDiff'] = df['Time'].diff().dt.total_seconds()
df['Speed'] = df['Last'].diff() / df['TimeDiff']
df['Acceleration'] = df['Speed'].diff() / df['TimeDiff']
df['Distance'] = df['Last'].diff().cumsum()
df.drop(columns=['TimeDiff'], inplace=True)

# Identify support and resistance
support_levels = []
resistance_levels = []

for i in range(1, len(df) - 1):
    if df['Low'][i] < df['Low'][i - 1] and df['Low'][i] < df['Low'][i + 1]:
        support_levels.append(i)
    if df['High'][i] > df['High'][i - 1] and df['High'][i] > df['High'][i + 1]:
        resistance_levels.append(i)

df['Support'] = 0
df['Support'].iloc[support_levels] = 1
df['Resistance'] = 0
df['Resistance'].iloc[resistance_levels] = 1

# Calculate VWAP (Volume-Weighted Average Price) 
df['VWAP'] = (df['Last'] * df['Volume']).cumsum() / df['Volume'].cumsum()

df.to_csv('./storage/2022altered_sierra.csv', index=False)

elapsed_time = time.time() - start_time

print(elapsed_time)

# took 4.1 hours to process 2022sierra_tick.txt (66 mil rows)