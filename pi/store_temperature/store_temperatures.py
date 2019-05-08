import arrow
import boto3
import requests
import json
import datetime
import logging

logger = logging.getLogger(__name__)

sqs = boto3.resource('sqs')
ddb = boto3.client('dynamodb')

queue = sqs.get_queue_by_name(QueueName='temperatures')

# keep trying till the queue is empty
while True:
    messages = queue.receive_messages(MaxNumberOfMessages=10,WaitTimeSeconds=20)
    # retrieve SQS messages
    if not messages:
        print("nothing to write")
        break
    # list to delete all messages at once
    delete_message_ids = []
    for message in messages:
        try:
            entries = json.loads(message.body)
        except:
            logger.exception("Exception while parsing queue data:", body)
        else:
            print("Got messages")
            logger.info(entries)
            for one_entry in entries:
                dt_obj = arrow.get(datetime.datetime.strptime(one_entry['status_time'], '%Y-%m-%d %I:%M:%S %p')).replace(tzinfo='America/New_York').to('utc')
                dt_str = dt_obj.isoformat()

                key_name = 'temperature+{}+{}'.format(one_entry['sensor_name'].upper(), dt_obj.date().strftime('%Y%m%d'))
                ddb.put_item(TableName='dataTable', Item={
                    'key_name': {"S": key_name},
                    'timestamp': {"S": dt_str },
                    'reading_value': {"N" : str(one_entry['raw_value']) }
                    }, ReturnConsumedCapacity='TOTAL')

                print("Inserted entry")

            delete_message_ids.append({'Id': message.message_id, 'ReceiptHandle': message.receipt_handle})
    queue.delete_messages(Entries=delete_message_ids)
