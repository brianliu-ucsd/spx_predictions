import pandas as pd
from IPython.display import display
import matplotlib.pyplot as plt
import time 
import numpy as np

start_time = time.time()

# This file contains code with a different method of storing support and resistance data

# Store support + resistance over different time periods
# Store support + resistance as time periods rather than distinct points

# One day's data
df = pd.read_csv('./storage/v2_2022altered_sierra_tick.csv')

# Use old support + resistance identifiers

# Keep track of current support and current resistance

# Have counters for times breached and times not reached for supports + resistances

# Have sensitivity, so that when certain times breached/not reached, support or resistance is changed accordingly
# to average of the breached/not reached

# Have buffer to prevent overcorrection: buffer around each support level, so that small
# variations don't unnecessarily sway level

df['Support'] = 0
df['Resistance'] = 0

support_level = df['Low'].iloc[0]
resistance_level = df['High'].iloc[0]

support_breached = []
support_not_reached = []
resistance_breached = []
resistance_not_reached = []

sensitivity = 5
buffer = 0.5

for i in range(1, len(df) - 1):
    low = df['Low'][i]
    high = df['High'][i]

    # Support reached
    if low < df['Low'][i - 1] and low < df['Low'][i + 1]:
        # Support breached
        if low < support_level - buffer:
            support_breached.append(low)
            # Sensitivity reached, update support_level
            if len(support_breached) >= sensitivity:
                support_breached.append(support_level)
                support_level = np.mean(support_breached)
                support_breached = []
                support_not_reached = []
        # Support not reached
        elif low > support_level + buffer:
            support_not_reached.append(low)
            # Sensitivity reached, update support_level
            if len(support_not_reached) >= sensitivity:
                support_not_reached.append(support_level)
                support_level = np.mean(support_not_reached)
                support_not_reached = []
                support_breached = []

    # Resistance reached
    if high > df['High'][i - 1] and high > df['High'][i + 1]:
        # Resistance breached
        if high > resistance_level + buffer:
            resistance_breached.append(high)
            # Sensitivity reached, update resistance_level
            if len(resistance_breached) >= sensitivity:
                resistance_breached.append(resistance_level)
                resistance_level = np.mean(resistance_breached)
                resistance_breached = []
                resistance_not_reached = []
        # Resistance not reached
        elif high < resistance_level - buffer:
            resistance_not_reached.append(high)
            # Sensitivity reached, updated resistance_level
            if len(resistance_not_reached) >= sensitivity:
                resistance_not_reached.append(resistance_level)
                resistance_level = np.mean(resistance_not_reached)
                resistance_not_reached = []
                resistance_breached = []

    df.at[i, 'Support'] = support_level
    df.at[i, 'Resistance'] = resistance_level

df.to_csv('v2_2022altered_sierra_tick.csv', index=False) 

# plt.plot(df['Time'], df['Last'], label='Last Price', color='blue')
# plt.show()

print(time.time() - start_time)