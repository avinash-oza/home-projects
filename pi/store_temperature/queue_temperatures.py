import argparse

import boto3
import requests


def main(endpoint_url):
    sqs = boto3.resource('sqs')

    queue = sqs.get_queue_by_name(QueueName='temperatures')

    try:
        body = requests.get(endpoint_url, timeout=2)
    except Exception as e:
        print("Exception when trying to pull url {}".format(endpoint_url))
    else:
        queue.send_message(MessageBody=body.text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--endpoint', default="http://localhost:25002/temperature/all")
    args = parser.parse_args()

    main(args.endpoint)
