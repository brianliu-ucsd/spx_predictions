import pandas as pd
from IPython.display import display

a = pd.read_csv('./../storage/21milrows/v3_21milrows.csv')
b = pd.read_csv('./../storage/v2_altered_sierra_tick.csv')

print('read')

drop_cols = ['Open','High','Low','Last','Volume','NumberOfTrades','BidVolume','AskVolume']
b = b.drop(columns=drop_cols)

print('dropped')

result = pd.concat([a,b], axis=1)

print('merged')

desired_order = ['DateTime', 'Open', 'High', 'Low', 'Last', 'Volume', 'NumberOfTrades', 'BidVolume', 'AskVolume', 'Speed', 'Acceleration', 'Distance', 'VWAP', 'Support', 'Resistance']
result = result[desired_order]

print('ordered')

result.to_csv('./../storage/21milrows/v4_21milrows.csv', index=False)