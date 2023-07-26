import os
import boto3
import logging

__logger = logging.getLogger()
__logger.setLevel(logging.INFO)

__dynamodb_table_name = os.getenv('USER_TABLE_NAME')
__dynamodb = boto3.client('dynamodb')


def lambda_handler(event: dict, context: dict) -> dict:
    """
    The event handler/entrypoint for this lambda.

    The lambda will delete a user from the DynamoDB database.
    """
    __logger.info(f'Lambda was invoked with event: {event}')

    user_id: str = event['user_id']

    response = __dynamodb.delete_item(
        TableName=__dynamodb_table_name,
        Key={
            'user_id': {'S': user_id}
        }
    )
    __logger.info(f'Received response: {response}')

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        __logger.info(f'The users information was successfully deleted from the table.')
        return format_return_message(200, user_id)
    # If the response code is not 200 something went wrong with DynamoDB.
    # Return an error message to the user
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
