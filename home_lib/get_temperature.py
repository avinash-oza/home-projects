import sys
import re
import ConfigParser
import time
import argparse
import subprocess

CRITICAL_TEMP = 73.0

def get_ds18b20_sensor(sensor_id):
    command_to_run="""cat /sys/bus/w1/devices/{0}/w1_slave""".format(sensor_id)
    output = subprocess.check_output([command_to_run], shell=True)
    filter_string = 't=(\d+)'
    found_matches = re.search(filter_string, output)
#   temperature = re.search('t=(\d+)', output).group(1)
    temperature = output.rsplit('=', 1)[1].strip()

    # Convert temperature to F
    f_degrees = 1.8*float(temperature)/1000 + 32
    # Write the temperature to DB
    print "Case Temperature: {0}F".format(f_degrees)
    if f_degrees > CRITICAL_TEMP:
        return 2
    else:
        return 0

if __name__ == '__main__':
    get_ds18b20_sensor('28-05167155beff')

