#!/usr/bin/python
import sys


def parse_float(value: str):
    return '%.2f' % float(value.replace('\"', ''))


def analyze_line(line: str):
    line = line.strip()
    columns = line.split(',')

    # device	ts	humidity	temp	light	motion	lpg	co	smoke	msg_received	metadata	__dt
    device_name = columns[0]
    humidity = columns[2]
    temperature = columns[3]
    received_at = columns[9]

    try:
        humidity = parse_float(humidity)
        temperature = parse_float(temperature)
        received_at = received_at.replace('\"', '')

        results = [device_name, received_at, humidity, temperature]
        results = tuple(results)
        output = ','.join(results)

        print(output)
    except Exception as e:
        pass


def main(argv):
    line = sys.stdin.readline()
    try:
        while line:
            analyze_line(line)
            line = sys.stdin.readline()
    except "end of file":
        return None


if __name__ == "__main__":
    main(sys.argv)
