import os
import json
import boto3
import logging

__logger = logging.getLogger()
__logger.setLevel(logging.INFO)

__dynamodb_table_name = os.getenv('patient_TABLE_NAME')
__dynamodb = boto3.client('dynamodb')


def lambda_handler(event: dict, context: dict) -> dict:
    """
    The event handler/entrypoint for this lambda.

    The lambda will update a patient in the DynamoDB database.
    """
    __logger.info(f'Lambda was invoked with event: {event}')
    body: dict = json.loads(json.dumps(event))

    keys = body.keys()
    expression: str = 'SET'
    values: dict = dict()

    # Parse the keys that are trying to be updated into a dict
    for key in keys:
        if key != 'patient_id':
            expression += f' {key}=:{key},'
            values.update({
                f':{key}': {'S': body[key]}
            })
    # There will be a trailing , at the end of expression, we need to remove it to avoid an error
    expression: str = expression[:-1]

    __logger.info(expression)
    __logger.info(values)

    response: dict = __dynamodb.update_item(
        TableName=__dynamodb_table_name,
        Key={'patient_id': {'S': event['patient_id']}},
        UpdateExpression=expression,
        ExpressionAttributeValues=values
    )
    __logger.info(f'Received response: {response}')

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        __logger.info(f'patient information was successfully updated in the database.')
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html; charset=utf-8"},
            "body": "Success"
        }
    # If the response code is not 200 something went wrong with DynamoDB.
    # Return an error message to the patient
    else:
        __logger.error(
            f"Something went wrong updating the patient. Received status: {response['ResponseMetadata']['HTTPStatusCode']}.")
        return format_return_message(response['ResponseMetadata']['HTTPStatusCode'],
                                     "Something went wrong with DynamoDB. Please try again later.")


def format_return_message(status: int, body: str) -> dict:
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
