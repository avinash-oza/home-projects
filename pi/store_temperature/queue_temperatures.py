import boto3
import requests


urls_to_get = ['http://172.16.2.100:25002/temperature/all', 'http://172.16.2.102:25002/temperature/all']

sqs = boto3.resource('sqs')

queue = sqs.get_queue_by_name(QueueName='temperatures')

for url in urls_to_get:
    try:
        body = requests.get(url, timeout=2)
    except Exception as e:
        print("Exception when trying to pull url {}".format(url))
    else:
        queue.send_message(MessageBody=body.text)
