# TODO save local parameters in external file

from configparser import ConfigParser
from elasticsearch import Elasticsearch
from df2json import df2json
import time
import json

# Setup
f = ConfigParser()
f.read('setup_db.ini')  # Parses the setup_db.ini file

host = f.get('database', 'host')
port = f.get('database', 'port')
index = str(f.get('database', 'index'))
doc_type = str(f.get('database', 'doc_type'))

raw_data_file = str(f.get('files', 'raw_data_file'))

period = f.getint('wait_time', 'period') / 1000  # Times is in milliseconds


# Connection to the ElasticSearch cluster
print('Connecting to ElasticSearch database...')
es = Elasticsearch([{'host': host,'port': port}])
print('Connection successful.')


# Data processing cycle
with open('last.date', 'r') as s:
    last = s.read()# Another setup file, used to save the date of the last reading that has been sent to the database

print('Starting data processing cycle...')

while True:
    # Raw data file processing (raw to dataframe, then dataframe to json)
    data = df2json(raw_data_file)
    print('Raw data loaded and processed.')

    # Adds to the ElasticSearch database the previously loaded data
    print('Starting POSTs...')
    for e in data:
        if last < e['date']:  # Adds new data to database only if more recent than the last item added (saved in the specific file last.date)
            es.index(index=index, doc_type=doc_type, body=e, id=e['date'])  # Adds element to DB with the date as unique id
            last = e['date']
        else:
            pass

    with open('last.date', 'w') as s:
        s.write(last)# Another setup file, used to save the date of the last reading that has been sent to the database

    print('Data has been successfully added to database.')

    time.sleep(period)
