import pika
import requests
import json
import mysql.connector
import configparser
import datetime

config = configparser.ConfigParser()
config.read('store_temperature.config')

credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
parameters = pika.URLParameters('amqp://rabbitmq:rabbitmq@192.168.122.1:5672')

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='temperatures_mysql')

db_host = config.get('DATABASE', 'host')
db_user_name = config.get('DATABASE', 'user')
db_password = config.get('DATABASE', 'password')
db_name = config.get('DATABASE', 'database')
db_connection = mysql.connector.connect(user=db_user_name,password=db_password,host=db_host, database=db_name)
db_connection.autocommit = True

def print_message(ch, method, properties, body):
    try:
        entries = json.loads(body)
    except:
        print("Exception while parsing queue data:", body)
    else:
        cursor = db_connection.cursor()
        for one_entry in entries:
            today = datetime.date.today()
            time = datetime.datetime.strptime(one_entry['status_time'], "%I:%M:%S%p").time()
            one_entry['formatted_time'] = datetime.datetime.combine(today, time)

            query = "INSERT INTO temperature.temperatures(sensor_name, sensor_value, reading_time) VALUES (%(sensor_name)s, %(raw_value)s, %(formatted_time)s)"
            cursor.execute(query, one_entry)

        print("Inserted entry")

channel.basic_consume(print_message, queue='temperatures_mysql', no_ack=True)

channel.start_consuming()
