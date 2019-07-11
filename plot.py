import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
from process_data import process_data
register_matplotlib_converters()

# Data loading and processing
df = process_data('data_test')  # Loads the processed data from the specified file

df = df.reset_index()  # Resets the index to a column; useful for plotting
df = df.set_index(['index'])  # Sets the date column as index
# df = df.loc['2019-07-11 13:00:00.000':'2019-07-11 14:00:00.000']  # Prints only the data from the selected time interval

df = df.reset_index()  # Resets the index to a column; useful for plotting
df['index'] = pd.to_datetime(df['index'], format='%Y-%m-%d %H:%M:%S.%f')  # Converts the index to a date format


# Plot settings
# noinspection PyTypeChecker
fig, axes = plt.subplots(nrows=4, ncols=1, sharex=True, figsize=(9, 6))
plt.gcf().canvas.set_window_title('SensorTag CC2650')
plt.gcf().autofmt_xdate()  # Rotation
axes[0].xaxis.set_major_locator(mdates.MinuteLocator(interval=10))


# Plots

# Ambient temperature
axes[0].plot(df['index'], df['temp'])
axes[0].set(ylabel='temperature (°C)', title='Environmental variables')
axes[0].xaxis.set_major_formatter(mdates.DateFormatter('%h %d - %H:%M'))

df_0 = process_data('data2')  # Loads the processed data from the specified file

df = df_0.reset_index()  # Resets the index to a column; useful for plotting

df.plot(x='index', y='temp')
plt.show()

df.plot(x='index', y='opt')
plt.show()
