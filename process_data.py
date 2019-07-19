from configparser import ConfigParser
from elasticsearch import Elasticsearch
from datetime import datetime
from modules import update_db as u
from modules import min_date as m
from modules import increase_day as i
import time
import os

# Setup
f = ConfigParser()
f.read('config/setup_db.ini')  # Parses the setup_db.ini file

host = f.get('database', 'host')
port = f.get('database', 'port')
index = str(f.get('database', 'index'))
doc_type = str(f.get('database', 'doc_type'))

period = f.getint('wait_time', 'period') / 1000  # Times is in milliseconds


# Connection to the ElasticSearch cluster
print('Connecting to ElasticSearch database...')
es = Elasticsearch([{'host': host,'port': port}])
print('Connection successful.')


# Raw data file selection
with open('config/last.date', 'r') as f:
    last_dates = eval(f.read())
min_date = m.min_date(last_dates)  # Finds the last day the database has been updated (for any device)

date = min_date
raw_data_file = min_date + '.log'  # The script will start adding entries to the database from the last day it updated it

# Data processing cycle
today = str(datetime.now())[0:10]

print('')

# Old logs retireval
status = False
print('Checking for old logs...')
while today > date:
    path = './logs/' + raw_data_file

    if os.path.isfile(path):  # Checks if the log exists...
        u.update_db(raw_data_file, last_dates, es, index, doc_type)  # This function will also rewrite the last day the database has been updated (the min)
        status = True
    else:  # ...otherwise just goes to the next day, and continues checking
        pass

    date = i.increase_day(date)
    raw_data_file = date + '.log'

print('Old logs check successful.')
if status:
    print('No old logs found.')
else:
    print('Old logs successfully added to database.')

print('')

# Current day loading
print('Starting data processing loop.')

print('')

try:
    while True:
        print('Checking for new data...')
        if today[8:10] < str(datetime.now())[8:10]:  # Checks if the day has changed (increased)
            today = str(datetime.now())[0:10]
            raw_data_file = today + '.log'
        else:
            pass

        up_status = u.update_db(raw_data_file, last_dates, es, index, doc_type)  # Updates the database with data from raw_data_file

        if up_status:
            print('Data has been successfully added to database. (' + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%s'))[:-7] + ')')
        else:
            print('No new data found. (' + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%s'))[:-7] + ')')

        print('Waiting for next check...\n')

        time.sleep(period)

except(KeyboardInterrupt):
    print('\n Stopped by user. Database is not being updated anymore.')
