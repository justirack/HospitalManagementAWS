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
    __logger.info(f'This lambda was invoked with event: {event}')

    # If no body exists return to avoid an error being thrown
    if event['body'] is None:
        __logger.info(
            'The request does not contain a body. Please add a body that includes a first name,'
            ' last name and date of birth. Returning 400 status code.')

        __bad_request.update({
            "body": "The request must contain a body, which must contain a first name, last name and date of birth."
        })
        return __bad_request

    body = json.loads(event['body'])

    # Make sure all patient data is included in the request, return if something is missing
    if "first_name" not in body:
        __logger.info(f'The request does not contain a first name. Returning 400 status code.')
        __bad_request.update({
            "body": "The patient could not be added as first_name was not defined"
        })
        return __bad_request

    if "last_name" not in body:
        __logger.info(f'The request does not contain a last name. Returning 400 status code.')
        __bad_request.update({
            "body": "The patient could not be added as last_name was not defined"
        })
        return __bad_request

    if "date_of_birth" not in body:
        __logger.info(f'The request does not contain a date of birth. Returning 400 status code.')
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

    response_payload = json.load(response["Payload"])
    __logger.info(f'Received response: {response_payload}')

    # If the status code is 200 return a success message
    if response['StatusCode'] == 200:
        __logger.info(f'The patient was successfully added to the database. Returning 200 status code.')
        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'text/html; charset=utf-8'
            },
            "body": json.dumps({
                "message": "The patient was successfully added to the database",
                "patient_id": response_payload["patient_id"]
            })

        }

    __logger.info(f'Something went wrong adding the patient to the database. Returning 500 status code.')
    return {
        "statusCode": 500,
        "headers": {
            'Content-Type': 'text/html; charset=utf-8',
        },
        "body": "Something went wrong adding the client to the database."
    }
