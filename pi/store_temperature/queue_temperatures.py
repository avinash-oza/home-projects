import pika
import requests

urls_to_get = ['http://172.16.2.100:25002/temperature/all', 'http://172.16.2.102:25002/temperature/all']

credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
parameters = pika.URLParameters('amqp://rabbitmq:rabbitmq@172.16.1.10:5672')

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.exchange_declare(exchange='temperatures', exchange_type='fanout')
channel.queue_declare(queue='temperatures_mysql')
channel.queue_declare(queue='temperatures_elasticsearch')
channel.queue_bind(exchange='temperatures', queue='temperatures_mysql')
channel.queue_bind(exchange='temperatures', queue='temperatures_elasticsearch')

for url in urls_to_get:
    body = requests.get(url) #TODO: Test
    channel.basic_publish(exchange='temperatures', routing_key='', body=body.text)
