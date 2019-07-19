def raw2df(raw_data_file):

    from configparser import ConfigParser
    import pandas as pd

    # Modules import and column definition
    f = ConfigParser()
    path = './config/setup.ini' + raw_data_file
    f.read('config/setup.ini')  # Parses the setup.ini file

    device_mac = str(f.get('device_mac', 'value'))

    cols = []
    i = 0
    for item in f.items('data_handles'):  # Reads the available type of retrievable data
        if(item[0] == 'mov'):  # Ignores the movement sensor
            pass
        else:
            cols.append(item[0])  # Creates the column list
            exec('from sensors.{0} import {0}'.format(cols[i]))  # Dynamically imports the sensor modules
            i = i + 1  # Does this really need an explanation?

    cols.append('MAC')  # Aggiunge la colonna del MAC del dispositivo che ha effettuato la lettura


    # Dataframe creation
    h = open(raw_data_file, 'r')  # Opens the data file in read mode

    ls = []
    for x in h:  # Creates a list with all available data
        ls.append(x[:-1])

    h.close()

    res = str(ls).replace('[', '{').replace(']', '}').replace('"', '')  # Replaces a few characters in the retrieved data to transform it in a Python dictionary


    # Dataframe
    df = pd.DataFrame.from_dict(res, orient='index')  # Defines the dataframe
    df = df.drop(['mov'], axis=1)
    df.index.name = 'index'  # Sets the index column name

    for i in range(0,  len(cols)):  # Processes the data for each column (= sensor type) with the available sensor modules (= processing algorithms)
        if cols[i] is not 'MAC':  # Ignores the MAC column (it needs no processing)
            df[cols[i]] = round(df[cols[i]].map(eval(cols[i])), 2)

    return df
