import os
import json
import boto3
import logging

__logger = logging.getLogger()
__logger.setLevel(logging.INFO)

__dynamodb_table_name = os.getenv('USER_TABLE_NAME')
__dynamodb = boto3.client('dynamodb')


def lambda_handler(event, context):
    __logger.info(f'Lambda was invoked with event: {event}')
    body = json.loads(json.dumps(event))

    payload = {}
    keys = body.keys()
    __logger.info(f'Payload: {payload}')
    __logger.info(f'Keys: {keys}')

    expression = 'SET'
    values = dict()

    for key in keys:
        if key != 'user_id':
            expression += f' {key}=:{key},'
            values.update({
                f':{key}': {'S': body[key]}
            })
    # There will be a trailing , at the end of expression, we need to remove it to avoid an error
    expression = expression[:-1]

    __logger.info(expression)
    __logger.info(values)

    response = __dynamodb.update_item(
        TableName=__dynamodb_table_name,
        Key={'user_id': {'S': event['user_id']}},
        UpdateExpression=expression,
        ExpressionAttributeValues=values
    )
    __logger.info(f'Received response: {response}')

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        __logger.info(f'User information was successfully updated in the database.')
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html; charset=utf-8"},
            "body": "Success"
        }
    # If the response code is not 200 something went wrong with DynamoDB.
    # Return an error message to the user
    else:
        __logger.error(
            f"Something went wrong updating the patient. Received status: {response['ResponseMetadata']['HTTPStatusCode']}.")
        return {
            "statusCode": response['ResponseMetadata']['HTTPStatusCode'],
            "headers": {"Content-Type": "text/html; charset=utf-8"},
            "body": "Something went wrong with DynamoDB. Please try again later."
        }

