import boto3
import os
import logging

__DYNAMO_DB_TABLE_NAME = os.getenv('PATIENT_TABLE_NAME')

dynamodb = boto3.client('dynamodb')

__logger = logging.getLogger()
__logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    __logger.info(f'This lambda was invoked with event {event}')

    patient_id = event

    response = dynamodb.query(
        TableName=__DYNAMO_DB_TABLE_NAME,
        KeyConditionExpression='patient_id = :patient_id',
        ExpressionAttributeValues={
            ':patient_id': {'S': patient_id}
        }
    )
    __logger.info(f'Received response: {response}')

    # If no patients are found return None
    if response['Count'] == 0:
        __logger.info("Returning None, no results found.")
        return None

    patients = list()

    # Add all patients that are returned to a list to return
    for patient in response['Items']:
        patients.append({
            "first_name": patient['first_name']['S'],
            "last_name": patient['last_name']['S'],
            "date_of_birth": patient['date_of_birth']['S']
        })

    __logger.info(f'Returning patients: {patients}')
    return patients
