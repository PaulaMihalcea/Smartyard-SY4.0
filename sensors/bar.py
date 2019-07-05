# TODO Refactor as class

raw_bar_data = '48 0a 00 d0 89 01'  # Here's the data received from the sensor
raw_bar_bytes = raw_bar_data.split()  # Splits the data string into bytes

bar_int = int('0x' + raw_bar_bytes[5] + raw_bar_bytes[4] + raw_bar_bytes[3], 16)  # Conversion from hex to int
bar_temp_int = int('0x' + raw_bar_bytes[2] + raw_bar_bytes[1] + raw_bar_bytes[0], 16)  # Conversion from hex to int

bar = float(bar_int) / 100  # Conversion to float and division as per TI algorithm
bar_temp = float(bar_temp_int) / 100  # Conversion to float and division as per TI algorithm

print('Barometric pressure: ' + str(bar) + ' hPa')
print('Temperature (barometric pressure sensor): ' + str(bar_temp) + '° C')
