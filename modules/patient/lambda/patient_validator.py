import os
import json
import boto3
import logging

__logger = logging.getLogger()
__logger.setLevel(logging.INFO)

__base_path = '/v1/patient/'

__lambda = boto3.client('lambda')
__patient_retrieval_lambda_arn = os.getenv('RETRIEVE_PATIENT_LAMBDA_INVOKE_URL')

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
        __logger.info('Invoked by the get endpoint. Trying to retrieve a patient from the database.')

        try:
            dict_contains_item(event['queryStringParameters'], 'id')
        except AssertionError as error:
            __logger.error(f'Error was raised validating contents of event: {error}')
            return format_return_message(400, str(error))

        response = __lambda.invoke(
            FunctionName=__patient_retrieval_lambda_arn,
            InvocationType="RequestResponse",
            Payload=json.dumps(event['queryStringParameters']['id'])
        )
        patients = json.load(response["Payload"])

        if response['StatusCode'] == 200 and patients is not None:
            __logger.info(f'Retrieved {len(patients)} from the database.')
            return format_return_message(200, json.dumps(patients))
        else:
            return format_return_message(500, "Something went wrong. Please try again later.")
    else:
        __logger.info(f'Invoked by an unknown endpoint: {path}')
        format_return_message(500, f'Invoked by an unknown endpoint: {path}')


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

