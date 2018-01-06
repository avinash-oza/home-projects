import pika
import requests
import configparser
import datetime
import json

# Gets data from the darksky api

config = configparser.ConfigParser()
config.read('store_temperature.config')


credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
parameters = pika.URLParameters('amqp://rabbitmq:rabbitmq@172.16.1.10:5672')

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.exchange_declare(exchange='temperatures', exchange_type='fanout')
channel.queue_declare(queue='temperatures_mysql')
channel.queue_declare(queue='temperatures_elasticsearch')
channel.queue_bind(exchange='temperatures', queue='temperatures_mysql')
channel.queue_bind(exchange='temperatures', queue='temperatures_elasticsearch')

dark_sky_api_key = config.get('DARKSKY', 'api_key')
location_coordinates = config.get('DARKSKY', 'location_coordinates')
url = "https://api.darksky.net/forecast/{0}/{1}?exclude=minutely,hourly,daily,alerts,flags".format(dark_sky_api_key, location_coordinates)

data = requests.get(url).json()

data_dict = dict(sensor_name="OUTDOOR",
                 raw_value=data['currently']['temperature'],
                 status_time=datetime.datetime.now().strftime('%Y-%m-%d %I:%M:%S %p'),
                 current_temperature=True)
channel.basic_publish(exchange='temperatures', routing_key='', body=json.dumps([data_dict]))
