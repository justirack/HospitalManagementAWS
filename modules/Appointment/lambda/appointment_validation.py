import logging

from typing import Union

__logger = logging.getLogger()
__logger.setLevel(logging.INFO)

__base_path = '/v1/appointment/'


def lambda_handler(event: dict, context: dict) -> dict:
    """
    The event handler/entrypoint for this lambda.

    The lambda will validate the contents of the event
    based on which endpoint it was invoked from.
    """

    __logger.info(f'Lambda was invoked with: {event}')

    path: str = event['path']

    # Handle a request to add a patient to the database
    if path == __base_path + 'book':
        return book_appointment(event)

    # Handle a request to get a patient from the database
    elif path == __base_path + 'get':
        return get_appointments(event)

    # Handle a request to update a patient in the database
    elif path == __base_path + 'update':
        return update_appointment(event)

    # Handle a request to remove a patient from the database
    elif path == __base_path + 'cancel':
        return cancel_appointment(event)
        # Handle a request from an unknown endpoint
    else:
        __logger.error(f'Invoked by an unknown endpoint: {path}')
        return format_return_message(500, 'The validation lambda was invoked from an unknown endpoint.')


def book_appointment(event: dict):
    return format_return_message(200, "booking endpoing")


def get_appointments(event: dict):
    return format_return_message(200, "Get endpoint")


def update_appointment(event: dict):
    return format_return_message(200, "update endpoint")


def cancel_appointment(event: dict):
    return format_return_message(200, "Cancel endpoint")


def format_return_message(status: int, body: Union[dict, str]) -> dict:
    """
    Formats a return json for the lambda function.

    :param status: The status code integer of the response.
    :param body: The string body of the response.
    :return: A json blob that can be returned from the lambda function.
    """

    return {
        "statusCode": status,
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST,PATCH,OPTIONS'},
        "body": body}
