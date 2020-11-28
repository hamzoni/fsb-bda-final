#!/usr/bin/env python
import sys
import time
import datetime
import dateutil.parser

storage = {}

f = open('result.txt', 'w')


def compare_timestamp(ts_x: str, ts_y: str, is_larger: bool):
    ts_x_d = dateutil.parser.parse(ts_x)
    ts_y_d = dateutil.parser.parse(ts_y)
    return ts_x if (ts_x_d > ts_y_d if is_larger else ts_x_d <= ts_y_d) else ts_y


def compare_number(input_x: str, input_y: str, is_larger: bool):
    val_x = float(input_x)
    val_y = float(input_y)
    return val_x if (val_x > val_y if is_larger else val_x <= val_y) else val_y


def calculate_average(input_x: float, input_y: float) -> float:
    result = (input_x + input_y) / 2
    result = '%.2f' % result
    return float(result)


for line in sys.stdin:
    line = line.strip()
    columns = line.split(',')

    # device_name, received_at, humidity, temperature
    device_name = columns[0]
    received_at = columns[1]
    humidity = columns[2]
    temperature = columns[3]

    if device_name not in storage or not storage[device_name]:
        storage[device_name] = {
            'last_received_at': received_at,
            'first_received_at': received_at,
            'temperature': {
                'average': float(temperature),
                'highest': float(temperature),
                'lowest': float(temperature),
            },
            'humidity': {
                'average': float(humidity),
                'highest': float(humidity),
                'lowest': float(humidity),
            },
        }
    else:
        storage[device_name]['last_received_at'] = compare_timestamp(
            storage[device_name]['last_received_at'], received_at, True
        )
        storage[device_name]['first_received_at'] = compare_timestamp(
            storage[device_name]['first_received_at'], received_at, False
        )

        storage[device_name]['humidity']['highest'] = compare_number(
            storage[device_name]['humidity']['lowest'], humidity, True
        )
        storage[device_name]['humidity']['highest'] = compare_number(
            storage[device_name]['humidity']['lowest'], humidity, False
        )
        storage[device_name]['humidity']['average'] = calculate_average(
            storage[device_name]['humidity']['average'], float(humidity)
        )

        storage[device_name]['temperature']['highest'] = compare_number(
            storage[device_name]['temperature']['lowest'], temperature, True
        )
        storage[device_name]['temperature']['highest'] = compare_number(
            storage[device_name]['temperature']['lowest'], temperature, False
        )
        storage[device_name]['temperature']['average'] = calculate_average(
            storage[device_name]['temperature']['average'], float(temperature)
        )

for attr, value in storage.items():
    print(attr, value)

f.close()
