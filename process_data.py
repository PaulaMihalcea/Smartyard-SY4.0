from configparser import ConfigParser  # For reading the setup file (config/setup_db.ini)
from elasticsearch import Elasticsearch  # For... well, the ElasticSearch server
from datetime import datetime  # For the current time
from modules import update_db as u  # For updating the database
from modules import min_date as m  # For finding the oldest date in which the db has been updated
from modules import increase_day as i  # For (correctly) increasing the day and proceed with the parsing of old logs
from modules import check_file as c  # For checking if the log for the current date actually exists
import time  # For the sleep() method
import os  # For checking if a log actually exists (and thus avoid errors if they don't)
import sys  # For getting the setup_db file as a command line argument

# Setup
f = ConfigParser()
setup_file_number = str(sys.argv[1])
if int(setup_file_number) == 1:
    f.read('config/setup_db.ini')  # Parses the setup_db.ini file
else:
    f.read('config/setup_db' + setup_file_number + '.ini')  # Parses the setup_db.ini file with the corresponding number (e.g. setup_db2.ini, etc.)

host = f.get('database', 'host')
port = f.get('database', 'port')
index = str(f.get('database', 'index'))
doc_type = str(f.get('database', 'doc_type'))

period = f.getint('wait_time', 'period') / 1000  # Time is in milliseconds
attempts = f.getint('wait_time', 'attempts')  # Number of attempts before exiting if no new logs have been found (typically needed when the sensor device has stopped working but this script is

logs_path = f.get('logs_path', 'value')

# Connection to the ElasticSearch cluster
print('Connecting to ElasticSearch database...')
es = Elasticsearch([{'host': host, 'port': port}])
print('Connection successful.')


# Raw data file selection
attempt_no = 1  # Number of attempts to read the last.dates file; the whole following block is a fix to an EOF exception that appears at times when trying to read the said file
while True:
    try:
        with open('config/last.date', 'r') as f:
            last_dates = eval(f.read())
    except Exception:
        print('Error while trying to read last.dates file, waiting for next check... (attempt no. ' + str(attempt_no) + '/' + str(attempts) + ')')
        attempt_no += 1
        time.sleep(period)
        if attempt_no > attempts:
            print('Error while trying to read last.dates file, maximum number of attempts reached. Exiting program.')
            exit()
        else:
            continue
    else:
        break

min_date = m.min_date(last_dates)  # Finds the last day the database has been updated (for any device)

date = min_date
raw_data_file = min_date + '.log'  # The script will start adding entries to the database from the last day it updated it


# Data processing cycle begins
today = str(datetime.now())[0:10]  # Current date

print('')


# Old logs retrieval
status = False  # Flag for telling the user if old logs have been added to the database (or not)
print('Checking for old logs...')
while today > date:
    raw_data_file_path = './' + logs_path + '/' + raw_data_file  # Dynamic path of the log file

    if os.path.isfile(raw_data_file_path):  # Checks if the log exists...
        u.update_db(raw_data_file_path, es, index, doc_type, attempts, period)  # This function will also rewrite the last day the database has been updated (the min)
        status = True  # The database has been updated, so we're letting the user know it
    else:  # ...otherwise just goes to the next day, and continues checking
        pass

    date = i.increase_day(date)  # Increases the current day (current = the one that has just been checked, which is older than the actual current day)
    raw_data_file = date + '.log'  # And updates the raw data file name to be checked

print('Old logs check successful.')  # Some pretty prints to reassure the user (and in the beginning me, too)
if status:
    print('Old logs successfully added to database.')
else:
    print('No old logs found.')

print('')


# Current day loading
print('Starting data processing loop.')

print('')

try:
    while True:
        print('Checking for new data...')

        if today[8:10] < str(datetime.now())[8:10]:  # Checks if the day has changed (increased)
            today = str(datetime.now())[0:10]
            raw_data_file = today + '.log'  # Updates the log file to read if midnight has passed
        else:
            pass

        raw_data_file_path = './' + logs_path + '/' + raw_data_file  # Dynamic path of the log file
        exists = c.check_file(raw_data_file_path, attempts, period)  # Checks if the log for the new day has been created

        if exists:
            up_status = u.update_db(raw_data_file_path, es, index, doc_type, attempts, period)  # Updates the database with data from raw_data_file
        else:  # No log with the current date has been found; after a number of attempts (specified in the variable "attempts"), the program automatically exists
            print('Exiting program.')
            exit()

        if up_status:
            print('Data has been successfully added to database. (' + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%s'))[:-7] + ')')  # More pretty prints for the user
        else:
            print('No new data found. (' + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%s'))[:-7] + ')')

        print('Waiting for next check...\n')

        time.sleep(period)  # Waits for the next check

except KeyboardInterrupt:
    print('\n Stopped by user. Database is not being updated anymore. Exiting program.')
    exit()
