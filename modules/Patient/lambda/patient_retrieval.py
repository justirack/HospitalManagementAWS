import boto3
import os
import logging

from typing import Union

__dynamodb_table_name = os.getenv('PATIENT_TABLE_NAME')
__dynamodb = boto3.client('dynamodb')

__logger = logging.getLogger()
__logger.setLevel(logging.INFO)


def lambda_handler(event: str, context: dict) -> Union[None, list]:
    """
    The event handler/entrypoint for this lambda.

    The lambda will retrieve a patient from the DynamoDB database.
    """
    __logger.info(f'Lambda was invoked with the event: {event}')
    patient_id: str = event

    response: dict = __dynamodb.query(
        TableName=__dynamodb_table_name,
        KeyConditionExpression='patient_id = :patient_id',
        ExpressionAttributeValues={
            ':patient_id': {'S': patient_id}
        }
    )
    __logger.info(f'Received response: {response}')

    # If no patients with the id are found, return None
    if response['Count'] == 0:
        __logger.info(f'Did not find any patients, returning None.')
        return None

    # Add all patients to a list to return them
    patients: list = list()
    for patient in response['Items']:
        patients.append({
            "first_name": patient['first_name']['S'],
            "last_name": patient['last_name']['S'],
            "date_of_birth": patient['date_of_birth']['S'],
            "phone_number": patient['phone_number']['S']
        })

        __logger.info(f'Returning patients: {patients}')
        return patients
