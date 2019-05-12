import json
import datetime
import arrow
import boto3

ddb = boto3.client('dynamodb')


def lambda_handler(event, context):
    for one_record in event['Records']:
        try:
            entries = json.loads(one_record['body'])
        except:
            print("Exception when parsing message", one_record)
        else:
            print("Got messages")
            for one_entry in entries:
                dt_obj = arrow.get(datetime.datetime.strptime(one_entry['status_time'], '%Y-%m-%d %I:%M:%S %p')).replace(tzinfo='America/New_York').to('utc')
                dt_str = dt_obj.isoformat()

                key_name = 'temperature+{}+{}'.format(one_entry['sensor_name'].upper(), dt_obj.date().strftime('%Y%m%d'))
                ddb.put_item(TableName='dataTable', Item={
                    'key_name': {"S": key_name},
                    'timestamp': {"S": dt_str },
                    'reading_value': {"N" : str(one_entry['raw_value']) }
                    }, ReturnConsumedCapacity='TOTAL')


test_events= {'Records': [{'messageId': '19dd0b57-b21e-4ac1-bd88-01bbb068cb78',
       'receiptHandle': 'MessageReceiptHandle',
          'body': '[{"raw_value": 67.325, "sensor_name": "GARAGE", "hostname": "pi2", "return_code": "0", "plugin_output": "Garage Temperature: 67.325F", "service_description": "Garage Temperature", "status_time": "2019-05-09 09:20:05 PM"}]',
             'attributes': {'ApproximateReceiveCount': '1',
                     'SentTimestamp': '1523232000000',
                         'SenderId': '123456789012',
                             'ApproximateFirstReceiveTimestamp': '1523232000001'},
                'messageAttributes': {},
                   'md5OfBody': '7b270e59b47ff90a553787216d55d91d',
                      'eventSource': 'aws:sqs',
                         'eventSourceARN': 'arn:aws:sqs:us-east-1:123456789012:MyQueue',
                            'awsRegion': 'us-east-1'},
                              {'messageId': '19dd0b57-b21e-4ac1-bd88-01bbb068cb78',
                                     'receiptHandle': 'MessageReceiptHandle',
                                     'body': '[{"raw_value": 67.325, "sensor_name": "GARAGE", "hostname": "pi2", "return_code": "0", "plugin_output": "Garage Temperature: 67.325F", "service_description": "Garage Temperature", "status_time": "2019-05-09 09:20:05 PM"}]',
                                           'attributes': {'ApproximateReceiveCount': '1',
                                                   'SentTimestamp': '1523232000000',
                                                       'SenderId': '123456789012',
                                                           'ApproximateFirstReceiveTimestamp': '1523232000001'},
                                              'messageAttributes': {},
                                                 'md5OfBody': '7b270e59b47ff90a553787216d55d91d',
                                                    'eventSource': 'aws:sqs',
                                                       'eventSourceARN': 'arn:aws:sqs:us-east-1:123456789012:MyQueue',
                                                          'awsRegion': 'us-east-1'}]}

#ambda_handler(test_events, None)
