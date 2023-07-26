import os
import json
import uuid
import boto3
import logging

__dynamodb_table_name = os.getenv('PATIENT_TABLE_NAME')
__dynamodb = boto3.client('dynamodb')

__logger = logging.getLogger()
__logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """
    The event handler/entrypoint for this lambda.

    This lambda will add a patient to the dynamoDB table.
    It will use a UUID as the source id and a combination of first name,
    last name and date of birth as the sort key.
    """
    __logger.info(f"This lambda was invoked with event: {event}")

    for record in event['Records']:
        body = json.loads(record['body'])
        __logger.info(body)

        patient_id = str(uuid.uuid4())
        sort_key = body['first_name'][0] + body['last_name'][0] + body['date_of_birth']

        response = __dynamodb.put_item(
            TableName=__dynamodb_table_name,
            Item={
                "patient_id": {'S': patient_id},
                'sort_key': {'S': sort_key},
                'first_name': {'S': body['first_name']},
                'last_name': {'S': body['last_name']},
                "date_of_birth": {'S': body['date_of_birth']}
            }
        )
        __logger.info(f"Received response: {response}")

        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            __logger.info("Patient was successfully added to database")
        else:
            __logger.warning(f"Something went wrong adding the patient. Received status: {response['ResponseMetadata']['HTTPStatusCode']}.")