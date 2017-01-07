import subprocess
import re

CRITICAL_TEMP = 71.0

class TemperatureReciever(object):
    """Retrieves temperatures from the sensors"""
    def get_case_temperature(self):
        command_to_run="""cat /sys/bus/w1/devices/28-000004f236cf/w1_slave"""
        output = subprocess.check_output([command_to_run], shell=True)
        filter_string = 't=(\d+)'
        found_matches = re.search(filter_string, output)
        # Multiple matches are coming. TODO: Figure out how to extract the string required. Original command was grep -oP 't=\s*\K\d+'
        temperature = re.search('t=(\d+)', output).group(1)

        # Convert temperature to F
        f_degrees = 1.8*float(temperature)/1000 + 32
        print "Case Temperature: {0}F".format(f_degrees)
        if f_degrees > CRITICAL_TEMP:
            exit(2)
        else:
            exit(0)

if __name__ == '__main__':
    o = TemperatureReciever()
    o.get_case_temperature();
