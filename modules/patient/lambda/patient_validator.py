import os
import json
import boto3
import logging

__logger = logging.getLogger()
__logger.setLevel(logging.INFO)

__base_path = '/v1/patient/'

__sqs = boto3.client('sqs')
__create_patient_queue_url = os.getenv('CREATE_PATIENT_QUEUE_URL')


def lambda_handler(event, context):
    """
    The event handler/entrypoint for this lambda.

    The lambda will validate the contents of the event
    based on which endpoint it was invoked from.
    """
    __logger.info(f'Lambda was invoked with: {event}')

    path = event['path']
    body = event['body']

    # Will have this logic for each endpoint
    if path == __base_path + 'add':
        __logger.info('Invoked by the add endpoint. Trying to add a patient to the database.')

        try:
            dict_contains_item(body, 'first_name')
            dict_contains_item(body, 'last_name')
            dict_contains_item(body, 'date_of_birth')
        except AssertionError as error:
            __logger.error(f'Error was raised validating contents of event: {error}')
            return format_return_message(400, str(error))

        response = send_message_to_queue(__create_patient_queue_url, event['body'])

        __logger.info(f'Response: {response}')
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return format_return_message(200, "The patient will be added to the database")
        else:
            return format_return_message(500, "Something went wrong. Please try again later.")
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
    """
    Checks if dict_to_check contains item
    Will raise an AssertionError if dict_to_check does not contain the item

    :param dict_to_check: A dictionary to check for an item in.
    :param item: The item to check the dictionary for.
    :return: True, or an error will be raised.
    """
    if item not in dict_to_check:
        raise AssertionError(f'The request must contain {item} in order to process successfully.')


def send_message_to_queue(queue_url, body):
    """
    Sends a message to the queue with url queue_url

    :param queue_url: The url of the queue to send the message to.
    :param body: The body of the message.
    :return: The response from SQS.
    """
    response = __sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=body
    )

    __logger.info(f'Response from SQS: {response}')
    return response


def format_return_message(status, body):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "text/html; charset=utf-8"},
        "body": body}

