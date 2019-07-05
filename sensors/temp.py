# TODO Refactor as class

class Temp:

    def temp(raw_temp_data):
        raw_temp_data = '50 0a 10 0d'  # Here's the data received from the sensor
        raw_temp_bytes = raw_temp_data.split()  # Splits the data string into bytes

        raw_ambient_temp = int('0x' + raw_temp_bytes[3] + raw_temp_bytes[2], 16)  # Conversion from hex to int
        ambient_temp_int = raw_ambient_temp >> 2  # Right shift (as per TI algorithm)
        ambient_temp_celsius = float(ambient_temp_int) * 0.03125  # Conversion to float and multiplication (as per TI algorithm)

        raw_obj_temp = int('0x' + raw_temp_bytes[1] + raw_temp_bytes[0], 16)  # Conversion from hex to int
        obj_temp_int = raw_obj_temp >> 2  # Right shift (as per TI algorithm)
        obj_temp_celsius = float(obj_temp_int) * 0.03125  # Conversion to float and multiplication (as per TI algorithm)

        return

    def get_ambient_temp_c():
        return ambient_temp_celsius

    def get_object_temp_c():
        return obj_temp_celsius

    return
