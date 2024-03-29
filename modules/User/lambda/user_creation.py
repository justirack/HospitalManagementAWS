import os
import json
import uuid
import boto3
import logging

from typing import Union

__logger = logging.getLogger()
__logger.setLevel(logging.INFO)

__dynamodb_table_name = os.getenv('USER_TABLE_NAME')
__dynamodb = boto3.client('dynamodb')


def lambda_handler(event: dict, context: dict) -> dict:
    """
    The event handler/entrypoint for this lambda.

    The lambda will add a user to the DynamoDB database.
    """
    __logger.info(f'Lambda was invoked with event: {event}')
    body: dict = json.loads(json.dumps(event))

    # Create the partition and sort keys for the new DynamoDB entry
    user_id: str = str(uuid.uuid4())

    # Make a call to DynamoDB attempting to add the user
    response: dict = __dynamodb.put_item(
        TableName=__dynamodb_table_name,
        Item={
            'user_id': {'S': user_id},
            'first_name': {'S': body['first_name']},
            'last_name': {'S': body['last_name']},
            'date_of_birth': {'S': body['date_of_birth']},
            'phone_number': {'S': body['phone_number']},
            'user_type': {'S': body['user_type']}
        }
    )
    __logger.info(f'Received response: {response}')

    # Return a response to the validation lambda depending on the status code received from DynamoDB
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        __logger.info("Patient was successfully added to database")
        return format_return_message(200, {'user_id': user_id})
    # If the response code is not 200 something went wrong with DynamoDB.
    # Return an error message to the user
    else:
        __logger.error(
            f"Something went wrong adding the patient. Received status: {response['ResponseMetadata']['HTTPStatusCode']}.")
        return format_return_message(response['ResponseMetadata']['HTTPStatusCode'],
                                     "Something went wrong with DynamoDB. Please try again later.")


def format_return_message(status: int, body: Union[str, dict]) -> dict:
    """
    Formats a return json for the lambda function.

    :param status: The status code integer of the response.
    :param body: The string body of the response.
    :return: A json blob that can be returned from the lambda function.
    """

    return {
        "statusCode": status,
        "headers": {"Content-Type": "text/html; charset=utf-8"},
        "body": body}
