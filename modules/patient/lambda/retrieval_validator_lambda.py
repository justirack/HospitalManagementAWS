import boto3
import json
import os
import logging

__PATIENT_RETRIEVER_LAMBDA_ARN = os.getenv('PATIENT_RETRIEVER_LAMBDA_ARN')

lambda_client = boto3.client('lambda')

__logger = logging.getLogger()
__logger.setLevel(logging.INFO)

__bad_request = {"statusCode": 400, "headers": {'Content-Type': 'text/html; charset=utf-8'}, "body": ""}


def lambda_handler(event, context):
    __logger.info(f'This lambda was invoked with event: {event}')

    # Make sure it will be possible to search the table
    if 'id' not in event['queryStringParameters']:
        __logger.error(f'A patients id must be passed to retrieve it from the database')
        __bad_request.update({
            "body": "A patients id must be passed to retrieve it from the database"
        })
        return __bad_request

    # Invoke the lambda that will search for the patient
    __logger.info(f'Retrieving patient with id {event["queryStringParameters"]["id"]}')
    response = lambda_client.invoke(
        FunctionName=__PATIENT_RETRIEVER_LAMBDA_ARN,
        InvocationType="RequestResponse",
        Payload=json.dumps(event['queryStringParameters']['id'])
    )

    response_payload = json.load(response["Payload"])
    __logger.info(f'Received response: {response_payload}')

    if response_payload is not None:
        __logger.info(f'The patient was successfully added to the database. Returning 200 status code.')
        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'text/html; charset=utf-8'
            },
            "body": response_payload
        }

    __logger.info(f"No patient with the id {event['queryStringParameters']['id']} was found in the database")
    __bad_request.update({
        "body": f"No patient with the id {event['queryStringParameters']['id']} was found in the database"
    })
    return __bad_request