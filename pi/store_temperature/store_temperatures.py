import pika
import requests
import json
import mysql.connector
import configparser
import datetime
import logging

logger = logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read('store_temperature.config')

credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
parameters = pika.URLParameters('amqp://rabbitmq:rabbitmq@172.16.1.10:5672')

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='temperatures_mysql')

db_host = config.get('DATABASE', 'host')
db_user_name = config.get('DATABASE', 'user')
db_password = config.get('DATABASE', 'password')
db_name = config.get('DATABASE', 'database')
db_connection = mysql.connector.connect(user=db_user_name,password=db_password,host=db_host, database=db_name)

def print_message(ch, method, properties, body):
    try:
        entries = json.loads(body.decode())
    except:
        logger.exception("Exception while parsing queue data:", body)
    else:
        cursor = db_connection.cursor()
        logger.info(entries)
        for one_entry in entries:
            one_entry['formatted_time'] = datetime.datetime.strptime(one_entry['status_time'], "%Y-%m-%d %I:%M:%S %p")

            query = "INSERT INTO temperature.temperatures(sensor_name, sensor_value, reading_time) VALUES (%(sensor_name)s, %(raw_value)s, %(formatted_time)s)"
            cursor.execute(query, one_entry)
            db_connection.commit()
            logger.info("Inserted entry")


channel.basic_consume(print_message, queue='temperatures_mysql', no_ack=True)

channel.start_consuming()
