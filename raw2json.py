import pandas as pd
import json
from process_data import process_data
from configparser import ConfigParser

# Local variables
data_file = 'data_test'

# Column (and subplot) definition
f = ConfigParser()
f.read('setup.ini')  # Parses the setup.ini file

cols = []
i = 0
for item in f.items('data_handles'):  # Reads the available type of retrievable data
    if item[0] == 'mov':  # Ignores the movement sensor
        pass
    else:
        cols.append(item[0])  # Creates the column list


# Data loading and processing
df = process_data(data_file)  # Loads the processed data from the specified file

df.index.name = 'date'  # Sets the index column name
df = df.reset_index()  # Resets the index to a column; useful for plotting
# df = df.set_index(['index'])  # Sets the date column as index
# df = df.loc['2019-07-11 13:00:00.000':'2019-07-11 14:00:00.000']  # Prints only the data from the selected time interval

#df = df.reset_index()  # Resets the index to a column; useful for plotting
# df['index'] = pd.to_datetime(df['index'], format='%Y-%m-%d %H:%M:%S.%f')  # Converts the index to a date format

jdict = df.to_dict('records')

e1 = {
    'date': '2019-07-12 14:48:46.415',
    'opt': '10 00',
    'hum': '20 68 f8 61',
    'bar': 'a8 0a 00 2c 89 01',
    'mov': 'c3 ff 06 01 2d 00 35 00 16 00 91 f7 7c 03 00 ff 4d fe',
    'temp': 'd4 0a 74 0d'
}

j = 1
for i in jdict:
    i['id'] = j
    j = j + 1
    i = json.dumps(i)

# print(jdict)  # jdict è una lista di records json

# print(json.dumps(jdict))

#with open('json', 'w') as file:
#    json.dump(jdict, file)

with open('json', 'r') as j:
    json_data = json.load(j)
    print(json_data)
