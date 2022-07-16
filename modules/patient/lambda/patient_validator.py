import os
import json
import boto3
import logging

__logger = logging.getLogger()
__logger.setLevel(logging.INFO)

__sqs = boto3.client('sqs')

__base_path = '/v1/patient/'

__CREATE_PATIENT_QUEUE_URL = os.getenv('CREATE_PATIENT_QUEUE_URL')


def lambda_handler(event, context):
    __logger.info(f'Lambda was invoked with: {event}')

    path = event['path']
    body = event['body']

    if path == __base_path + 'add':
        __logger.info('Invoked by the add endpoint. Trying to add a patient to the database.')

        try:
            dict_contains_item(body, 'first_name')
            dict_contains_item(body, 'last_name')
            dict_contains_item(body, 'date_of_birth')
        except AttributeError as error:
            __logger.error(f'Error was raised: {error}')

        response = send_message_to_queue(__CREATE_PATIENT_QUEUE_URL, event['body'])

        __logger.info(f'Response: {response}')
    elif path == __base_path + 'get':
        __logger.info('Invoked by the get endpoint. Trying to get a patient from the database')

    return {
        "statusCode": 200,
        "headers": {
            'Content-Type': 'text/html; charset=utf-8'
        },
        "body": json.dumps({
            "message": "Success"
        })
    }


def dict_contains_item(dict_to_check, item):
    # Check if the item is in the dict, throw an error if not
    # Check GhostWriter code for example (release_consumer I think)

    # This isn't the correct syntax
    if item not in dict_to_check:
        raise AttributeError


def send_message_to_queue(queue_url, body):
    response = __sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(body)
    )

    __logger.info(f'Response from SQS: {response}')
    return response
