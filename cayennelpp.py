# -*- coding: utf-8 -*-
import base64
import binascii


def one_per_bit_unsigned(data):
    return int.from_bytes(data, byteorder='big', signed=False)


def point_zero_one_per_bit_signed(data):
    return int.from_bytes(data, byteorder='big', signed=True) / 100


def temperature(data):
    return int.from_bytes(data, byteorder='big', signed=True) / 10


def humidity(data):
    return int.from_bytes(data, byteorder='big', signed=False) / 2


def accelerometer(data):
    x = int.from_bytes(data[:2], byteorder='big', signed=True) / 1000
    y = int.from_bytes(data[2:4], byteorder='big', signed=True) / 1000
    z = int.from_bytes(data[4:6], byteorder='big', signed=True) / 1000

    return {'x': x, 'y': y, 'z': z}


def barometer(data):
    return int.from_bytes(data, byteorder='big', signed=False) / 10


def gyrometer(data):
    x = int.from_bytes(data[:2], byteorder='big', signed=True) / 100
    y = int.from_bytes(data[2:4], byteorder='big', signed=True) / 100
    z = int.from_bytes(data[4:6], byteorder='big', signed=True) / 100

    return {'x': x, 'y': y, 'z': z}


def gps_location(data):
    lat = int.from_bytes(data[:3], byteorder='big', signed=True) / 10000
    lon = int.from_bytes(data[3:6], byteorder='big', signed=True) / 10000
    alt = int.from_bytes(data[6:], byteorder='big', signed=True) / 100

    return {'lat': lat, 'lon': lon, 'alt': alt}


DATA_TYPES = {
    b'\x00': {
        "name": "Digital Input",
        "size": 1,
        "decoder": one_per_bit_unsigned
    },
    b'\x01': {
        "name": "Digital Output",
        "size": 1,
        "decoder": one_per_bit_unsigned
    },
    b'\x02': {
        "name": "Analog Input",
        "size": 2,
        "decoder": point_zero_one_per_bit_signed
    },
    b'\x03': {
        "name": "Analog Output",
        "size": 2,
        "decoder": point_zero_one_per_bit_signed
    },
    b'\x65': {
        "name": "Illuminance Sensor",
        "size": 2,
        "decoder": one_per_bit_unsigned
    },
    b'\x66': {
        "name": "Presence Sensor",
        "size": 1,
        "decoder": one_per_bit_unsigned
    },
    b'\x67': {
        "name": "Temperature Sensor",
        "size": 2,
        "decoder": temperature
    },
    b'\x68': {
        "name": "Humidity Sensor",
        "size": 1,
        "decoder": humidity
    },
    b'\x71': {
        "name": "Accelerometer",
        "size": 6,
        "decoder": accelerometer
    },
    b'\x73': {
        "name": "Barometer",
        "size": 2,
        "decoder": barometer
    },
    b'\x86': {
        "name": "Gyrometer",
        "size": 6,
        "decoder": gyrometer
    },
    b'\x88': {
        "name": "GPS Location",
        "size": 9,
        "decoder": gps_location
    },
}


def lppdecode(base64_string):
    cursor = 0
    result = []
    payload = base64.b64decode(base64_string)

    while cursor < len(payload):
        data_channel = int.from_bytes(payload[cursor:cursor + 1],
                                      byteorder='big')
        cursor += 1
        data_type = payload[cursor:cursor + 1]
        if data_type in DATA_TYPES:
            cursor += 1
            name = DATA_TYPES[data_type]['name']
            size = DATA_TYPES[data_type]['size']
            decoder = DATA_TYPES[data_type]['decoder']
            result.append(
                {"channel": data_channel,
                 "type": name,
                 "value": decoder(payload[cursor:cursor + size])})
            cursor += size
        else:
            # Unknown LPP data type
            result = None
            break

    return result
