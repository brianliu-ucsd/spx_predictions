import pandas as pd
from IPython.display import display

chunk_size = 1000000
chunk_dfs = []

for chunk in pd.read_csv('./storage/2022altered_sierra.csv', chunksize=chunk_size):

    print(chunk.iloc[0])

    # Create an empty list to store the combined DateTime values
    date_times = []

    # Iterate through each row
    for index, row in chunk.iterrows():
        date = row['Date']
        time = row['Time'].split(' ')[-1]
        date_time = pd.to_datetime(date + ' ' + time)
        date_times.append(date_time)

    # Add the list as a new column to the DataFrame
    chunk['DateTime'] = date_times

    # Drop the original "Date" and "Time" columns
    chunk.drop(['Date', 'Time'], axis=1, inplace=True)

    chunk_dfs.append(chunk)

# df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'].str.split(' ').str[-1])

# df.drop(['Date', 'Time'], axis=1, inplace=True)

# col = df.pop('DateTime')
# df.insert(0, 'DateTime', col)  

final = pd.concat(chunk_dfs, ignore_index=True) 

col = final.pop('DateTime')
final.insert(0, 'DateTime', col) 

final.to_csv('./storage/v2_2022altered_sierra_tick.csv', index=False)