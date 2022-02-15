import boto3
import logging
import os

__DYNAMO_DB_TABLE_NAME = os.getenv('PATIENT_TABLE_NAME')

dynamodb = boto3.client('dynamodb')

__logger = logging.getLogger()
__logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    __logger.info("This lambda was invoked with event: %s", event)

    response = dynamodb.put_item(
        TableName=__DYNAMO_DB_TABLE_NAME,
        Item={
            "patient_id": {'S': '192636'},
            'sort_key': {'S': 'JR020902'},
            'firstName': {'S': 'Justin'},
            'lastName': {'S': 'Rackley'}
        }
    )

    __logger.info("Received response: %s", response)

    return response
