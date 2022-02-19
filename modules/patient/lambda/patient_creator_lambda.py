import boto3
import logging
import os
import uuid

__DYNAMO_DB_TABLE_NAME = os.getenv('PATIENT_TABLE_NAME')

dynamodb = boto3.client('dynamodb')

__logger = logging.getLogger()
__logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    __logger.info("This lambda was invoked with event: %s", event)

    sort_key = event['first_name'][0] + event['last_name'][0] + event['date_of_birth']

    response = dynamodb.put_item(
        TableName=__DYNAMO_DB_TABLE_NAME,
        Item={
            "patient_id": {'S': str(uuid.uuid4())},
            'sort_key': {'S': sort_key},
            'first_name': {'S': event['first_name']},
            'last_name': {'S': event['last_name']},
            "date_of_birth": {'S': event['date_of_birth']}
        }
    )

    __logger.info("Received response: %s", response)

    return response
