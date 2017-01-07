import sys
import subprocess
import re
import ConfigParser
import time
import argparse
import mysql.connector

config = ConfigParser.ConfigParser()
config.read('bot.config')

CRITICAL_TEMP = 71.0

class TemperatureReciever(object):
    """Retrieves temperatures from the sensors"""
    def __init__(self):
        db_host_name = config.get('DATABASE', 'host')
        db_user_name = config.get('DATABASE', 'user')
        db_password = config.get('DATABASE', 'password')
        database_name = config.get('DATABASE', 'database')

        # construct the connection object to use later
        self.conn =  mysql.connector.connect(user=db_user_name,password=db_password,host=db_host_name, database=database_name)

    def get_case_temperature(self):
        command_to_run="""cat /sys/bus/w1/devices/28-000004f236cf/w1_slave"""
        output = subprocess.check_output([command_to_run], shell=True)
        filter_string = 't=(\d+)'
        found_matches = re.search(filter_string, output)
        # Multiple matches are coming. TODO: Figure out how to extract the string required. Original command was grep -oP 't=\s*\K\d+'
        temperature = re.search('t=(\d+)', output).group(1)

        # Convert temperature to F
        f_degrees = 1.8*float(temperature)/1000 + 32
        # Write the temperature to DB
        self.store_temperature("CASE_TEMPERATURE", f_degrees)
        print "Case Temperature: {0}F".format(f_degrees)
        if f_degrees > CRITICAL_TEMP:
            return 2
        else:
            return 0

    def get_basement_temperature(self):
        # Put this in a loop as sometimes we do not get back a reading
        temperature = None
        humidity = None
        for tries in xrange(4):
            # Use utility to try and pull temperature and humidity
            command_to_run="""sudo /usr/local/nagios/libexec/AdafruitDHT 11 18"""
            output = subprocess.check_output([command_to_run], shell=True)
            if 'Temp' in output:
                c_temperature = self.extract_field_from_reading(output, 'Temp')
                temperature = 1.8*float(c_temperature) + 32
                humidity = self.extract_field_from_reading(output, 'Hum')
                break
            # Wait before retrying
            time.sleep(5)

        # Only store if the value came back valid
        if temperature and humidity:
            self.store_temperature("BASEMENT_TEMPERATURE", temperature)
            self.store_temperature("BASEMENT_HUMIDITY", humidity)
        print "Basement Temperature: {0}F Humidity {1} %".format(temperature, humidity)
        # TODO: Make actual constant
        if  temperature > CRITICAL_TEMP + 3:
            return 2
        else:
            return 0


    def extract_field_from_reading(self, output, string_to_search_for):
        # This is a good reading as we have the data we need
        reg_expression = '{0} = \d+'.format(string_to_search_for)
        first_string = re.search(reg_expression, output).group(0)
        # Take the temp out from this
        reading = re.search('\d+', first_string).group(0)

        return reading

    def store_temperature(self, sensor_name, sensor_value):
        # Write out the value to the db
        query = """INSERT INTO `temperatures`(sensor_name, sensor_value) VALUES('{0}', {1})""".format(sensor_name, sensor_value)
        cursor = self.conn.cursor(buffered=True)
        cursor.execute(query)
        # Commit the insert
        self.conn.commit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', action='store_true', help="Return the temperature inside the case")
    args = parser.parse_args()

    o = TemperatureReciever()
    if args.case:
        sys.exit(o.get_case_temperature())
    else:
        sys.exit(o.get_basement_temperature())
