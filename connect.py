from configparser import ConfigParser
import time
import pexpect

# Pexpect can be used for automating interactive applications.
# It allows the script to spawn a child application and control it as if a human were typing commands.
# In this application Pexpect is used to run and control the gatttool.


# Setup
f = ConfigParser()

f.read('setup.ini')  # Parses the setup.ini file

device_mac = f.get('device_mac', 'value')

timeout = f.getint('wait_time', 'timeout')
sleep = f.getint('wait_time', 'sleep')
period = f.getint('wait_time', 'period')

config_handles = []
for item in f.items("config_handles"):
    config_handles.append(item[1])

config_values = []
for item in f.items("config_values"):
    config_values.append(item)

data_handles = []
for item in f.items("data_handles"):
    data_handles.append(item[1])

data_length = []
for item in f.items("data_length"):
    data_length.append(item[1])


# Connection
child = pexpect.spawn('gatttool -I')  # Runs gatttool with the interactive option and returns the child process handle needed for further commands
child.sendline('connect {0}'.format(device_mac))  # connect 54:6C:0E:80:3F:01 (sends the string to the spawned process (gatttool))
child.expect('Connection successful', timeout)  # Waits for the "Connection successful" gatttool message; timeouts in the specified time


# Sensor configuration
for s in range(0, len(config_handles)):
    child.sendline('char-write-cmd {0} {1}'.format(config_handles[s], config_values[s][1]))  # char-write-cmd 0x00HH 0xCCCC (where HH is the BLE characteristic handle, while CC the configuration code; activates the desired sensor)
    time.sleep(0.5)  # Waits 0.5 seconds before sending next command to avoid flooding the BLE device


time.sleep(sleep)  # Waits a few seconds (recommended) to allow the device to turn its sensors on; if sleep == 0, the first readings might be wrong as the sensors would still be off


# Data retrieval cycle
raw_data = []

while True:
    for s in range(0, len(config_handles)):  # Data retrieval
        child.sendline('char-read-hnd {0}'.format(data_handles[s]))  # char-read-hnd 0x00HH (where HH is the BLE characteristic handle)

        child.expect('Characteristic value/descriptor: ', timeout)  # Waits for the first part of the output...
        child.expect("\r\n", timeout)  # ...then waits for the end of line

        raw_data.append(child.before[0:data_length[s]])  # Gets the output string just before the line end

        # TODO questi dati vanno salvati da qualche parte: dove? (e in che formato? -> dovrebbero essere facilmente plottabili)

        time.sleep(0.1)  # Waits before proceeding with the next sensor



    time.sleep(period / 1000)  # Repeats the data reading cycle every _period_ milliseconds
