# Device: TI SimpleLink SensorTag CC2650STK

#!/usr/bin/env python
# -*- coding: utf-8 -*-


def temp(raw_temp_data):
    # raw_temp_data = 'c8 0a 68 0d'  # Here's some test data received from the sensor
    raw_temp_bytes = raw_temp_data.split()  # Splits the data string into bytes

    raw_ambient_temp = int('0x' + raw_temp_bytes[3] + raw_temp_bytes[2], 16)  # Conversion from hex to int
    ambient_temp_int = raw_ambient_temp >> 2  # Right shift (as per TI algorithm)
    ambient_temp_celsius = float(ambient_temp_int) * 0.03125  # Conversion to float and multiplication (as per TI algorithm)

    # raw_obj_temp = int('0x' + raw_temp_bytes[1] + raw_temp_bytes[0], 16)  # Conversion from hex to int
    # obj_temp_int = raw_obj_temp >> 2  # Right shift (as per TI algorithm)
    # obj_temp_celsius = float(obj_temp_int) * 0.03125  # Conversion to float and multiplication (as per TI algorithm)

    # print('Ambient temperature: ' + str(ambient_temp_celsius) + '° C')
    # print('Object temperature: ' + str(obj_temp_celsius) + '° C')

    return ambient_temp_celsius
