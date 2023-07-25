import os
import re
import json
import boto3
import logging
import datetime

__logger = logging.getLogger()
__logger.setLevel(logging.INFO)

__base_path = '/v1/user/'

__updatable_information = ['user_id', 'first_name', 'last_name', 'date_of_birth', 'phone_number']

__lambda = boto3.client('lambda')
__user_retrieval_lambda_arn = os.getenv('RETRIEVE_USER_LAMBDA_INVOKE_URL')
__user_creation_lambda_arn = os.getenv('CREATE_USER_LAMBDA_INVOKE_URL')
__user_update_lambda_arn = os.getenv('UPDATE_USER_LAMBDA_INVOKE_URL')
__user_deletion_lambda_arn = os.getenv('DELETE_USER_LAMBDA_INVOKE_URL')

__regex = re.compile("^(([0-9]{10})|\([0-9]{3}\)(|\s)[0-9]{3}-[0-9]{4}|[0-9]{3}-[0-9]{3}-[0-9]{4}|[0-9]{3}\s[0-9]{3}\s[0-9]{4})$")


def lambda_handler(event: dict, context: dict):
    """
    The event handler/entrypoint for this lambda.

    The lambda will validate the contents of the event
    based on which endpoint it was invoked from.
    """
    __logger.info(f'Lambda was invoked with: {event}')

    path = event['path']

    # Handle a request to add a patient to the database
    if path == __base_path + 'add':
        return add_user(event)

    # Handle a request to get a patient from the database
    elif path == __base_path + 'get':
        return get_user(event)

    # Handle a request to update a patient in the database
    elif path == __base_path + 'update':
        return update_user(event)

    # Handle a request to remove a patient from the database
    elif path == __base_path + 'delete':
        return format_return_message(200, "Placeholder return until functionality for other lambdas is implemented.")

    # Handle a request from an unknown endpoint
    else:
        __logger.error(f'Invoked by an unknown endpoint: {path}')
        return format_return_message(500, 'The validation lambda was invoked from an unknown endpoint.')


def add_user(event: dict):
    """
    Validates that the request contains all required information, then adds a new user to the database.

    :param event: The event that the lambda function was invoked with, to be passed to the creation lambda.
    :return: JSON containing a status code, and string message.
    """
    __logger.info(f'Invoked by the add endpoint. Validating information in request.')
    body = dict()
    if event['body'] is not None:
        body = json.loads(event['body'])

    # Use the dict_contains_item function to make sure all required information is present in the request
    try:
        dict_contains_item(body, "first_name")
        dict_contains_item(body, 'last_name')
        dict_contains_item(body, 'date_of_birth')
        dict_contains_item(body, 'phone_number')
        dict_contains_item(body, 'user_type')

        validate_phone_number(body['phone_number'])
        datetime.date.fromisoformat(body['date_of_birth'])
    # If something is missing an error will be raised, catch it and return an error message to the user
    except AssertionError as error:
        __logger.error(f'An error was raised validating the contents of the request: {error}')
        return format_return_message(400, str(error))
    except ValueError as error:
        __logger.error(str(error))
        return format_return_message(400, str(error))

    # Invoke the creation lambda function. This will create a new record in the database.
    __logger.info(f'All required information is present. Adding patient to database.')
    response = __lambda.invoke(
        FunctionName=__user_creation_lambda_arn,
        InvocationType="RequestResponse",
        Payload=event['body']
    )
    __logger.info(f'Creation lambda returned: {response}')

    # Parse the body of the response, so it can be passed back to the user
    response_body = json.loads(response['Payload'].read())

    if response_body['statusCode'] == 200:
        # Parse the user id from the response, so it can be returned to the user
        user_id = response_body["body"]["user_id"]

        __logger.info(f'User was successfully added to the database. Their user ID is: {user_id}')
        return format_return_message(200, f'User was successfully added to the database. Their user ID is: {user_id}')
    # If the response code was not 200 something went wrong in the other lambda function,
    # return an error message to the user
    else:
        return format_return_message(response_body['statusCode'], response_body['body'])


def get_user(event: dict):
    """
    Validates a request to the get endpoint, then retrieves a user from the database.

    :param event: The event that the lambda function was invoked with, containing the user ID to search for.
    :return:JSON containing a status code, and a string message.
    """
    __logger.info(f'Invoked by the get endpoint. Validating request.')

    try:
        if event['queryStringParameters'] is None:
            raise AssertionError(f'The user id must be passed as a query string parameter.')
    except AssertionError as error:
        __logger.error(f'An error was raised validating the request: {error}')
        return format_return_message(400, str(error))

    response = __lambda.invoke(
        FunctionName=__user_retrieval_lambda_arn,
        InvocationType="RequestResponse",
        Payload=json.dumps(event['queryStringParameters']['id'])
    )
    __logger.info(f'Retrieval lambda returned: {response}')
    users = json.load(response['Payload'])

    if response['StatusCode'] == 200 and users is not None:
        __logger.info(f'Retrieved {len(users)} user(s) from the database. Returning them to the user.')
        return format_return_message(200, json.dumps(users))
    elif response['StatusCode'] == 200 and users is None:
        __logger.info(f'Did not find any users in the database')
        return format_return_message(200, "No users found.")
    else:
        __logger.info(f'Something went wrong. Try again later.')
        return format_return_message(response['StatusCode'], f'Something went wrong. Try again later.')


def update_user(event: dict):
    """
    Validates a request to the update endpoint, then updates a users' information in the database.

    :param event: The event that the lambda function was invoked with, containing.
    :return: JSON containing a status code, and a string message.
    """
    __logger.info(f'Invoked by the update endpoint. Validating request.')
    body = dict()
    if event['body'] is not None:
        body = json.loads(event['body'])

    try:
        keys = body.keys()
        __logger.info(f'Keys: {keys}')

        dict_contains_item(body, 'user_id')
        if body is None or not set(keys).issubset(set(__updatable_information)):
            raise AssertionError(f'The contents of the request are invalid')

    except AssertionError as error:
        return format_return_message(400, str(error))

    response = __lambda.invoke(
        FunctionName=__user_update_lambda_arn,
        InvocationType="RequestResponse",
        Payload=event['body']
    )
    __logger.info(f'Update lambda returned: {response}')

    response_body = json.loads(response['Payload'].read())
    __logger.info(response_body)

    return format_return_message(response_body['statusCode'], response_body['body'])


def dict_contains_item(check_dict: dict, item: str):
    """
    Checks if check_dict contains item as a key.
    Will raise an AssertionError if check_dict does not contain item.

    :param check_dict: A dictionary to search for a key value.
    :param item: A key value to search for in dict.
    :return: True if item is in check_dict, or an error will be raised.
    """

    if item not in check_dict:
        raise AssertionError(f'The request must contain {item} in order to be processed successfully.')


def format_return_message(status: int, body: str):
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


def validate_phone_number(number: str):
    """
    Uses a regex to ensure that a passed phone number is of a valid format.

    :param number: The phone number to be checked .
    :return: True if the phone number is valid, raise a ValueError if it is not.
    """
    if not __regex.match(number):
        raise ValueError(f'The phone number entered is not in a valid format.')
