import boto3
import requests
import json
import mysql.connector
import configparser
import datetime
import logging

logger = logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read('store_temperature.config')

db_host = config.get('DATABASE', 'host')
db_user_name = config.get('DATABASE', 'user')
db_password = config.get('DATABASE', 'password')
db_name = config.get('DATABASE', 'database')
db_connection = mysql.connector.connect(user=db_user_name,password=db_password,host=db_host, database=db_name)

sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='temperatures')

for message in queue.receive_messages(MaxNumberOfMessages=10,WaitTimeSeconds=20):
# retrieve SQS messages

    try:
        entries = json.loads(message.body)
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
        message.delete()
