# Device: TI SimpleLink SensorTag CC2650STK

#!/usr/bin/env python
# -*- coding: utf-8 -*-

def opt(raw_opt_data):

    # raw_opt_data = '59 8d'  # Here's some test data received from the sensor
    raw_opt_bytes = raw_opt_data.split()  # Splits the data string into bytes

    raw_opt = int('0x' + raw_opt_bytes[1] + raw_opt_bytes[0], 16)  # Conversion from hex to int

    m = raw_opt & 0x0FFF  # Masking as per TI algorithm
    e = (raw_opt & 0x0FFF) >> 12  # Masking and right shift as per TI algorithm

    if e == 0:  # Operations as per TI algorithm
        e = 1
    else:
        e = 2 << (e - 1)

    opt = m * (0.01 * e)  # More operations as per TI algorithm

    # print('Light intensity: ' + str(opt) + ' lx')

    return opt
