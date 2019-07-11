import matplotlib.pyplot as plt
import pandas as pd
from process_data import process_data

df_0 = process_data('data2')  # Loads the processed data from the specified file

df = df_0.reset_index()  # Resets the index to a column; useful for plotting

df.plot(x='index', y='temp')
plt.show()

df.plot(x='index', y='opt')
plt.show()
