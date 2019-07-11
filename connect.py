from configparser import ConfigParser
from datetime import datetime
import time
import pexpect

# Pexpect can be used for automating interactive applications.
# It allows the script to spawn a child application and control it as if a human were typing commands.
# In this application Pexpect is used to run and control the gatttool.


# Setup
status = False  # Status flag; remains false until a connection has been established

f = ConfigParser()

f.read('setup.ini')  # Parses the setup.ini file

device_mac = f.get('device_mac', 'value')

connection_timeout = f.getint('wait_time', 'connection_timeout') / 1000  # All times are in millseconds
data_timeout = f.getint('wait_time', 'data_timeout') / 1000
wait_after_config = f.getint('wait_time', 'wait_after_config') / 1000
time_between_sensor_configs = f.getint('wait_time', 'time_between_sensor_configs') / 1000
time_between_data_requests = f.getint('wait_time', 'time_between_data_requests') / 1000
period = f.getint('wait_time', 'period') / 1000

config_handles = []
for item in f.items('config_handles'):
    config_handles.append(item[1])

config_values = []
for item in f.items('config_values'):
    config_values.append(item)

data_handles = []
for item in f.items('data_handles'):
    data_handles.append(item)

data_length = []
for item in f.items('data_length'):
    data_length.append(item[1])

# Connection
try:
    child = pexpect.spawn('gatttool -I')  # Runs gatttool with the interactive option and returns the child process handle needed for further commands
    child.sendline('connect {0}'.format(device_mac))  # connect 54:6C:0E:80:3F:01 (sends the string to the spawned process (gatttool))
    print('Connecting to ' + str(device_mac) + '...')
    child.expect('Connection successful', connection_timeout)  # Waits for the "Connection successful" gatttool message; timeouts in the specified time
    status = True
    print('Connection successful.')

    # Sensor configuration
    print('Starting sensor configuration...')
    for s in range(0, len(config_handles)):
        child.sendline('char-write-cmd {0} {1}'.format(config_handles[s], config_values[s][1]))  # char-write-cmd 0x00HH 0xCCCC (where HH is the BLE characteristic handle, while CC the configuration code; activates the desired sensor)
        time.sleep(time_between_sensor_configs)  # Waits some seconds before sending next command to avoid flooding the BLE device
    print('Sensor configuration successful.')

    time.sleep(wait_after_config)  # Waits a few seconds (recommended) to allow the device to turn its sensors on; if sleep == 0, the first readings might be wrong as the sensors would still be off

    # Data retrieval cycle
    try:
        print('Data retrieval cycle started. Press CTRL+C to stop and disconnect.')
        while True:

            t = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Current date and time in human-readable format
            raw_data = {t: {}}  # Temporarily saves the new data as a dictionary

            parser = ConfigParser()
            parser.add_section(str(t))  # Adds a new section to the data file, named after the current date and time

            for s in range(0, len(config_handles)):  # Data retrieval
                child.sendline('char-read-hnd {0}'.format(data_handles[s][1]))  # char-read-hnd 0x00HH (where HH is the BLE characteristic handle)

                child.expect('Characteristic value/descriptor: ', data_timeout)  # Waits for the first part of the output...
                child.expect("\r\n", data_timeout)  # ...then waits for the end of line

                raw_data[t][str(data_handles[s][0])] = str(child.before[0:int(data_length[s])])  # Adds a new sensor-value pair to the temporary dictionary

                time.sleep(time_between_data_requests)  # Waits before proceeding with the next sensor

            with open('data', 'a') as f:
                f.write(str(raw_data)[1:-1] + '\n')  # Writes to the data file the raw data in a human-readable format, then adds a new line for the next reading

            time.sleep(period)  # Repeats the data reading cycle every _period_ milliseconds

    except(KeyboardInterrupt):
        print('\n Stopped by user. Data is not being received anymore.')
    finally:
        child.sendline('disconnect')  # Disconnects from the BLE device
        child.close(force=True)
        print('Disconnected.')
except(Exception):
    if status:
        print('Disconnected, device out of range. Exiting program.')
    else:
        print('Connection timed out. Exiting program.')
