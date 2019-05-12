import requests
import configparser
import datetime
import json
import boto3

# Gets data from the darksky api

config = configparser.ConfigParser()
config.read('store_temperature.config')


dark_sky_api_key = config.get('DARKSKY', 'api_key')
location_coordinates = config.get('DARKSKY', 'location_coordinates')
url = "https://api.darksky.net/forecast/{0}/{1}?exclude=minutely,hourly,daily,alerts,flags".format(dark_sky_api_key, location_coordinates)

try:
    data = requests.get(url, timeout=5).json()
except Exception as e:
    print("Exception occured getting data from dark sky")
else:
    # construct value for queue
    data_dict = dict(sensor_name="OUTDOOR",
                     raw_value=data['currently']['temperature'],
                     status_time=datetime.datetime.now().strftime('%Y-%m-%d %I:%M:%S %p'),
                     current_temperature=True)
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName='temperatures')
    queue.send_message(MessageBody=json.dumps([data_dict]))
