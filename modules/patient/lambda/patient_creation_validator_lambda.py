import boto3
import logging
import json
import os

__PATIENT_CREATOR_LAMBDA_ARN = os.getenv('PATIENT_CREATOR_LAMBDA_ARN')

lambda_client = boto3.client('lambda')

__logger = logging.getLogger()
__logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    __logger.info("This lambda was invoked with event: %s", event)

    response = lambda_client.invoke(
        FunctionName=__PATIENT_CREATOR_LAMBDA_ARN,
        InvocationType="RequestResponse",
        Payload=json.dumps(event )
    )

    __logger.info("Received response: %s", response)

    return {
           "statusCode": 200,
           "headers": {
               'Content-Type': 'text/html; charset=utf-8',
           },
           "body": "Hello world!"
            }
