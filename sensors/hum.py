# TODO Refactor as class

raw_hum_data = 'd8 66 34 4d'  # Here's the data received from the sensor
raw_hum_bytes = raw_hum_data.split()  # Splits the data string into bytes

raw_hum = int('0x' + raw_hum_bytes[3] + raw_hum_bytes[2], 16)  # Conversion from hex to int
raw_hum_temp = int('0x' + raw_hum_bytes[1] + raw_hum_bytes[0], 16)  # Conversion from hex to int

hum = (float(raw_hum) / 65536) * 100  # Conversion to float and division as per TI algorithm
hum_temp = (float(raw_hum_temp) / 65536) * 165 - 40  # Conversion to float and division as per TI algorithm

print('Relative Humidity: ' + str(hum) + '%')
print('Temperature (humidity sensor): ' + str(hum_temp) + '° C')
