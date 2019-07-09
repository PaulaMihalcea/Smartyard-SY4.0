import pandas as pd
import numpy as np
from datetime import datetime
import time

import sensors


d = ConfigParser()
s = ConfigParser()

d.read('data')  # Parses the data file
s.read('setup.ini')

sensor_names = []
for item in s.items('data_handles'):
    sensor_names.append(item[0])
    print(item[0])

# Lettura dei dati da file
raw_data = []
for s in sensor_names:
    raw_data.append()



for s in sensor_names:
    sensor_names.temp(raw_data)
