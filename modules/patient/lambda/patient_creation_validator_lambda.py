import boto3
import logging
import json
import os

__PATIENT_CREATOR_LAMBDA_ARN = os.getenv('PATIENT_CREATOR_LAMBDA_ARN')

lambda_client = boto3.client('lambda')

__logger = logging.getLogger()
__logger.setLevel(logging.INFO)

__bad_request = {"statusCode": 400, "headers": {'Content-Type': 'text/html; charset=utf-8'}, "body": ""}

def lambda_handler(event, context):
    __logger.info("This lambda was invoked with event: %s", event)

    body = json.loads(event['body'])

    # Make sure all patient data is included in the request
    if "first_name" not in  body:
        __bad_request.update({
            "body": "The patient could not be added as first_name was not defined"
        })
        return __bad_request

    if "last_name" not in  body:
        __bad_request.update({
            "body": "The patient could not be added as last_name was not defined"
        })
        return __bad_request

    if "date_of_birth" not in  body:
        __bad_request.update({
            "body": "The patient could not be added as date_of_birth was not defined"
        })
        return __bad_request

    # Send the patient data to the next lambda
    response = lambda_client.invoke(
        FunctionName=__PATIENT_CREATOR_LAMBDA_ARN,
        InvocationType="RequestResponse",
        Payload=json.dumps(body)
    )

    __logger.info("Received response: %s", response)

    if response['StatusCode'] != 200:
        return {
            "statusCode": 500,
            "headers": {
                'Content-Type': 'text/html; charset=utf-8',
            },
            "body": "Something went wrong adding the client to the database."
        }

    return {
        "statusCode": 200,
        "headers": {
            'Content-Type': 'text/html; charset=utf-8'
        },
        "body": "The patient was successfully added to the database",
        "patient_id": response['patient_id']}
