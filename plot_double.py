import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
from modules import raw2df as r
from configparser import ConfigParser
register_matplotlib_converters()

# Local variables
data_file_1 = 'logs/data_test'
data_file_2 = 'logs/data_test'
MAC_1 = '54:6C:0E:80:3F:01'
MAC_2 = '98:07:2D:32:23:80'
tick_interval = 10  # Time interval between ticks on the x axis, in minutes
window_title = 'SensorTag CC2650'  # Plot window title
ncols = 1  # Number of columns (for subplots)
nrows = 4  # Number of rows (for subplots)


# Column (and subplot) definition
f = ConfigParser()
f.read('config/setup.ini')  # Parses the setup.ini file

cols = []
i = 0
for item in f.items('data_handles'):  # Reads the available type of retrievable data
    if item[0] == 'mov':  # Ignores the movement sensor
        pass
    else:
        cols.append(item[0])  # Creates the column list


# Data loading and processing 1
df_1 = r.raw2df(data_file_1)  # Loads the processed data from the specified file

df_1 = df_1.reset_index()  # Resets the index to a column; useful for plotting
df_1 = df_1.set_index(['index'])  # Sets the date column as index
# df = df.loc['2019-07-11 13:00:00.000':'2019-07-11 14:00:00.000']  # Prints only the data from the selected time interval

df_1 = df_1.reset_index()  # Resets the index to a column; useful for plotting
df_1['index'] = pd.to_datetime(df_1['index'], format='%Y-%m-%d %H:%M:%S.%f')  # Converts the index to a date format

# Data loading and processing 2
df_2 = r.raw2df(data_file_2)  # Loads the processed data from the specified file

df_2 = df_2.reset_index()  # Resets the index to a column; useful for plotting
df_2 = df_2.set_index(['index'])  # Sets the date column as index
# df = df.loc['2019-07-11 13:00:00.000':'2019-07-11 14:00:00.000']  # Prints only the data from the selected time interval

df_2 = df_2.reset_index()  # Resets the index to a column; useful for plotting
df_2['index'] = pd.to_datetime(df_2['index'], format='%Y-%m-%d %H:%M:%S.%f')  # Converts the index to a date format


# Plot settings
fig, ax = plt.subplots(nrows=nrows, ncols=ncols, sharex=True, figsize=(9, 6))  # Plot definition, with number of subplots and layout
plt.gcf().canvas.set_window_title(window_title)  # Window title
plt.gcf().autofmt_xdate()  # Rotation
ax[0].xaxis.set_major_locator(mdates.MinuteLocator(interval=tick_interval))  # x axis tick interval


# Subplot creation
# NB This specific framework is valid for any plot with 4 subplots
for i in range(0, nrows):
    line_1, = ax[i].plot(df_1['index'], df_1[cols[i]])
    line_2, = ax[i].plot(df_2['index'], df_2[cols[i]])
fig.legend((line_1, line_2), (MAC_1, MAC_2), loc='lower center', ncol=2)


# x axis label formatter, in this case the same for all subplots. If sharex == True (when initially defining the plot), only one needs to be specified at any time
ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%h %d - %H:%M'))
# axes[1].xaxis.set_major_formatter(mdates.DateFormatter('%h %d - %H:%M'))
# axes[2].xaxis.set_major_formatter(mdates.DateFormatter('%h %d - %H:%M'))
# axes[3].xaxis.set_major_formatter(mdates.DateFormatter('%h %d - %H:%M'))


# Subplot labels
# NB These plots are specific to the SensorTag CC2560 STK device; more plots for different columns of the received dataframe can, however, be easily implemented
ax[0].set(ylabel='temperature (°C)', title='Environmental variables')  # Ambient temperature
ax[1].set(ylabel='humidity (%)')  # Humidity
ax[2].set(ylabel='pressure (hPa)')  # Pressure
ax[3].set(ylabel='light intensity (lx)')  # Light intensity

plt.show()
