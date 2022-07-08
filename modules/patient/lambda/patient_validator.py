import os
import json
import boto3
import logging

__logger = logging.getLogger()
__logger.setLevel(logging.INFO)

__CREATE_PATIENT_QUEUE_URL = os.getenv('PATIENT_TABLE_NAME')


def lambda_handler(event, context):
    __logger.info(f'Lambda was invoked with: {event}')

    send_message_to_queue(__CREATE_PATIENT_QUEUE_URL, "Test message body")


def send_message_to_queue(queue_url, body):
    queue = boto3.resource('sqs').Queue(queue_url)

    response = queue.send_message(
        MessageBody=json.dumps(body)
    )

    console.log(response)
    return response
