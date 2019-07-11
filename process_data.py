from configparser import ConfigParser
import pandas as pd

# Modules import and column definition
f = ConfigParser()
f.read('setup.ini')  # Parses the setup.ini file

cols = []
i = 0
for item in f.items('data_handles'):  # Reads the available type of retrievable data
    cols.append(item[0])  # Creates the column list
    exec('from sensors.{0} import {0}'.format(cols[i]))  # Dynamically imports the sensor modules
    i = i + 1  # Does this really need an explanation?


# Dataframe creation
h = open('data', 'r')  # Opens the data file in read mode

ls = []
for x in h:  # Creates a list with all available data
    ls.append(x[:-1])

res = eval(str(ls).replace('[', '{').replace(']', '}').replace('"', ''))  # Replaces a few characters in the retrieved data to transform it in a Python dictionary


# Dataframe
df = pd.DataFrame.from_dict(res, orient='index')  # Defines the dataframe

for i in range(0,  len(cols)):  # Processes the data for each column (= sensor type) with the available sensor modules (= processing algorithms)
    df[cols[i]] = round(df[cols[i]].map(eval(cols[i])), 2)

print(df)
#print(df['temp'])
