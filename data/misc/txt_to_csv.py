input_file_path = './../storage/2022sierra_tick.txt'
output_file_path = './../storage/2022sierra_tick.csv'

# Open the input text file in read mode
with open(input_file_path, 'r') as input_file:
    # Open the output CSV file in write mode
    with open(output_file_path, 'w') as output_file:
        # Write CSV headers
        output_file.write("Date,Time,Open,High,Low,Last,Volume,NumberOfTrades,BidVolume,AskVolume\n")  # Replace with your column names
        
        # Skip headers
        next(input_file)

        # Iterate thru input file and store in output
        for line in input_file:
            date, time, open, high, low, last, volume, numberoftrades, bidvolume, askvolume = line.split(', ')
            output_file.write(f"{date},{time},{open},{high},{low},{last},{volume},{numberoftrades},{bidvolume},{askvolume}")
                
print("Conversion completed.")