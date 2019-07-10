import pandas as pd
from datetime import datetime

# DATA SAVING (to file)
t = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

raw_data = {t: {}}  # Temporarily saves the new data as a dictionary

print(raw_data)


raw_data[t]['temp'] = '400'

print(raw_data)

raw_data[t]['hum'] = '100'

print(raw_data)

with open('data_test', 'a') as f:
    f.write(str(raw_data)[1:-1] + '\n')  # Writes to the data file the raw data in a human-readable format
    #f.write('\n')  # Adds a new line for the next reading


# DATA READING (from file)

h = open('data_test', 'r')

ls = []
for x in h:
    ls.append(x[:-1])

res = eval(str(ls).replace('[', '{').replace(']', '}').replace('"', ''))

dataframe = pd.DataFrame.from_dict(res, orient='index')
dataframe.reset_index(level=0, inplace=True)
print(dataframe)
