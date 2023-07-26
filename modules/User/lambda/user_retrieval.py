import boto3
import os
import logging

from typing import Union

__dynamodb_table_name = os.getenv('USER_TABLE_NAME')
__dynamodb = boto3.client('dynamodb')

__logger = logging.getLogger()
__logger.setLevel(logging.INFO)


def lambda_handler(event: str, context: dict) -> Union[None, list]:
    __logger.info(f'Lambda was invoked with the event: {event}')
    user_id: str = event

    response: dict = __dynamodb.query(
        TableName=__dynamodb_table_name,
        KeyConditionExpression='user_id = :user_id',
        ExpressionAttributeValues={
            ':user_id': {'S': user_id}
        }
    )
    __logger.info(f'Received response: {response}')

    # If no users with the id are found, return None
    if response['Count'] == 0:
        __logger.info(f'Did not find any users, returning None.')
        return None

    # Add all users to a list to return them
    users: list = list()
    for user in response['Items']:
        users.append({
            "first_name": user['first_name']['S'],
            "last_name": user['last_name']['S'],
            "date_of_birth": user['date_of_birth']['S']
        })

        __logger.info(f'Returning users: {users}')
        return users
