# TODO Split this script in three or return everything as an array
# Device: TI SimpleLink SensorTag CC2650STK
# NOTE: This is a multiple sensor, therefore multiple functions must be included in any script that processes its data

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Gyroscope


def gyro(raw_mov_data):
    # Data bytes
    # raw_mov_data = 'ad ff 27 01 00 00 00 02 4c 01 bc 3d 2f 01 8f ff 53 fe'  # Here's some test data received from the sensor
    raw_mov_bytes = raw_mov_data.split()  # Splits the data string into bytes

    # x axis
    gyro_x_int = int('0x' + raw_mov_bytes[1] + raw_mov_bytes[0], 16)  # Conversion from hex to int
    gyro_x = float(gyro_x_int) / (65536 / 500)  # Conversion to float and operations as per TI algorithm

    # y axis
    gyro_y_int = int('0x' + raw_mov_bytes[3] + raw_mov_bytes[2], 16)  # Conversion from hex to int
    gyro_y = float(gyro_y_int) / (65536 / 500)  # Conversion to float and operations as per TI algorithm

    # z axis
    gyro_z_int = int('0x' + raw_mov_bytes[5] + raw_mov_bytes[4], 16)  # Conversion from hex to int
    gyro_z = float(gyro_z_int) / (65536 / 500)  # Conversion to float and operations as per TI algorithm

    # print('Gyroscope      x: ' + str(gyro_x) + ' deg/s   y: ' + str(gyro_y) + ' deg/s   z: ' + str(gyro_z) + ' deg/s')

    return gyro_x, gyro_y, gyro_z


# Accelerometer
def acc(raw_mov_data):
    # Data bytes
    # raw_mov_data = 'ad ff 27 01 00 00 00 02 4c 01 bc 3d 2f 01 8f ff 53 fe'  # Here's some test data received from the sensor
    raw_mov_bytes = raw_mov_data.split()  # Splits the data string into bytes

    # Configuration bytes
    raw_config_data = '7f 03'  # Here's the current Config value of the sensor
    raw_config_bytes = raw_config_data.split()  # Splits the data string into bytes

    config_bytes = int('0x' + raw_config_bytes[1], 16)  # Conversion from hex to int
    config_bytes_bin = list(bin(config_bytes)[2:].zfill(
        8))  # Conversion from int to binary (every bit sets on or off a certain feature, so binary is easier to work with - see sensor Config tables)

    def acc_range(acc_a):  # Function needed to determine the necessary operation to process the data, as per TI algorithm
        acc_range_bit = int(config_bytes_bin[7] + config_bytes_bin[6],
                            2)  # Conversion from binary to int (to get the corresponding range value)

        if acc_range_bit == 0:
            r = 2
        elif acc_range_bit == 1:
            r = 4
        elif acc_range_bit == 2:
            r = 8
        elif acc_range_bit == 3:
            r = 16

        v = acc_a / (32768 / r)
        return v

     # x axis
    acc_x_f = float(int('0x' + raw_mov_bytes[7] + raw_mov_bytes[6], 16))  # Conversion from hex to int, then float
    acc_x = acc_range(acc_x_f)

    # y axis
    acc_y_f = float(int('0x' + raw_mov_bytes[9] + raw_mov_bytes[8], 16))  # Conversion from hex to int, then float
    acc_y = acc_range(acc_y_f)

    # z axis
    acc_z_f = float(int('0x' + raw_mov_bytes[11] + raw_mov_bytes[10], 16))  # Conversion from hex to int, then float
    acc_z = acc_range(acc_z_f)

    # print('Accelerometer  x: ' + str(acc_x) + ' G   y: ' + str(acc_y) + ' G   z: ' + str(acc_z) + ' G')

    return acc_x, acc_y, acc_z


# Magnetometer
def mag(raw_mov_data):
    # Data bytes
    # raw_mov_data = 'ad ff 27 01 00 00 00 02 4c 01 bc 3d 2f 01 8f ff 53 fe'  # Here's some test data received from the sensor
    raw_mov_bytes = raw_mov_data.split()  # Splits the data string into bytes

    # x axis
    mag_x = float(int('0x' + raw_mov_bytes[13] + raw_mov_bytes[12], 16))  # Conversion from hex to int, then float

    # y axis
    mag_y = float(int('0x' + raw_mov_bytes[15] + raw_mov_bytes[14], 16))  # Conversion from hex to int, then float

    # z axis
    mag_z = float(int('0x' + raw_mov_bytes[17] + raw_mov_bytes[16], 16))  # Conversion from hex to int, then float

    # print('Magnetometer   x: ' + str(mag_x) + ' uT   y: ' + str(mag_y) + ' uT   z: ' + str(mag_z) + ' uT')

    return mag_x, mag_y, mag_z
