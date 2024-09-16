import os
import re
import json
import boto3
import logging
import datetime

from typing import Union

__logger = logging.getLogger()
__logger.setLevel(logging.INFO)

__base_path = '/v1/patient/'
__updatable_information = ['patient_id', 'first_name', 'last_name', 'date_of_birth', 'phone_number']
__phone_regex = re.compile(
    "^(([0-9]{10})|\([0-9]{3}\)(|\s)[0-9]{3}-[0-9]{4}|[0-9]{3}-[0-9]{3}-[0-9]{4}|[0-9]{3}\s[0-9]{3}\s[0-9]{4})$")

__lambda = boto3.client('lambda')
__patient_retrieval_lambda_arn = os.getenv('RETRIEVE_PATIENT_LAMBDA_INVOKE_URL')
__patient_creation_lambda_arn = os.getenv('CREATE_PATIENT_INVOKE_URL')
__patient_update_lambda_arn = os.getenv('UPDATE_PATIENT_LAMBDA_INVOKE_URL')
__patient_deletion_lambda_arn = os.getenv('DELETE_PATIENT_LAMBDA_INVOKE_URL')

__REQUEST_RESPONSE_INVOCATION_TYPE = 'RequestResponse'


def lambda_handler(event: dict, context: dict) -> dict:
    """
    The event handler/entrypoint for this lambda.

    The lambda will validate the contents of the event
    based on which endpoint it was invoked from.
    """
    __logger.info(f'Lambda was invoked with: {event}')

    path: str = event['path']

    # Handle a request to add a patient to the database
    if path == __base_path + 'add':
        return add_patient(event)

    # Handle a request to get a patient from the database
    elif path == __base_path + 'get':
        return get_patient(event)

    # Handle a request to update a patient in the database
    elif path == __base_path + 'update':
        return update_patient(event)

    # Handle a request to remove a patient from the database
    elif path == __base_path + 'delete':
        return delete_patient(event)

    # Handle a request from an unknown endpoint
    else:
        __logger.error(f'Invoked by an unknown endpoint: {path}')
        return format_return_message(500, 'The validation lambda was invoked from an unknown endpoint.')


def add_patient(event: dict) -> dict:
    """
    Validates that the request contains all required information, then adds a new patient to the database.

    :param event: The event that the lambda function was invoked with, to be passed to the creation lambda.
    :return: JSON containing a status code, and string message.
    """
    __logger.info(f'Invoked by the add endpoint. Validating information in request.')
    body: dict = dict()
    if event['body'] is not None:
        body: dict = json.loads(event['body'])

    # Use the dict_contains_item function to make sure all required information is present in the request
    try:
        dict_contains_item(body, "first_name")
        dict_contains_item(body, 'last_name')
        dict_contains_item(body, 'date_of_birth')
        dict_contains_item(body, 'phone_number')
        dict_contains_item(body, 'patient_type')

        validate_phone_number(body['phone_number'])
        datetime.date.fromisoformat(body['date_of_birth'])
    # If something is missing an error will be raised, catch it and return an error message to the patient
    except AssertionError as error:
        __logger.error(f'An error was raised validating the contents of the request: {error}')
        return format_return_message(400, str(error))
    except ValueError as error:
        __logger.error(str(error))
        return format_return_message(400, str(error))

    # Invoke the creation lambda function. This will create a new record in the database.
    __logger.info(f'All required information is present. Adding patient to database.')
    response: dict = invoke_lambda(__patient_creation_lambda_arn,
                                   __REQUEST_RESPONSE_INVOCATION_TYPE,
                                   event['body'])
    __logger.info(f'Creation lambda returned: {response}')

    # Parse the body of the response, so it can be passed back to the patient
    response_body: dict = json.loads(response['Payload'].read())

    # Return different responses to the patient depending on what the retrieval lambda returned
    if response_body['statusCode'] == 200:
        # Parse the patient id from the response, so it can be returned to the patient
        patient_id: str = response_body["body"]["patient_id"]

        __logger.info(f'patient was successfully added to the database. Their patient ID is: {patient_id}')
        # return format_return_message(200, f'patient was successfully added to the database. Their patient ID is: {patient_id}')
        return format_return_message(200, json.dumps({"message": "patient was successfully added to the database",
                                                      "id": patient_id}))
    # If the response code was not 200 something went wrong in the other lambda function,
    # return an error message to the patient
    else:
        return format_return_message(response_body['statusCode'], response_body['body'])


def get_patient(event: dict) -> dict:
    """
    Validates a request to the get endpoint, then retrieves a patient from the database.

    :param event: The event that the lambda function was invoked with, containing the patient ID to search for.
    :return:JSON containing a status code, and a string message.
    """
    __logger.info(f'Invoked by the get endpoint. Validating request.')

    # Validate that the patient passed in a patient id in the request
    try:
        if event['queryStringParameters'] is None:
            raise AssertionError(f'The patient id must be passed as a query string parameter.')
    except AssertionError as error:
        __logger.error(f'An error was raised validating the request: {error}')
        return format_return_message(400, str(error))

    response: dict = invoke_lambda(__patient_retrieval_lambda_arn,
                                   __REQUEST_RESPONSE_INVOCATION_TYPE,
                                   json.dumps(event['queryStringParameters']['id']))

    __logger.info(f'Retrieval lambda returned: {response}')
    patients: dict = json.load(response['Payload'])

    # Return different responses to the patient depending on what the retrieval lambda returned
    if response['StatusCode'] == 200 and patients is not None:
        __logger.info(f'Retrieved {len(patients)} patient(s) from the database. Returning them to the patient.')
        return format_return_message(200, json.dumps(patients))
    elif response['StatusCode'] == 200 and patients is None:
        __logger.info(f'Did not find any patients in the database')
        return format_return_message(200, "No patients found.")
    else:
        __logger.info(f'Something went wrong. Try again later.')
        return format_return_message(response['StatusCode'], f'Something went wrong. Try again later.')


def update_patient(event: dict) -> dict:
    """
    Validates a request to the update endpoint, then updates a patients' information in the database.

    :param event: The event that the lambda function was invoked with, containing.
    :return: JSON containing a status code, and a string message.
    """

    "::TODO::"
    "Passing an ID that is now present in the table will create a new entry"
    "Validate that the ID exists before trying to update"

    __logger.info(f'Invoked by the update endpoint. Validating request.')
    body: dict = dict()
    if event['body'] is not None:
        body: dict = json.loads(event['body'])

    # Validate the information the patient passed
    try:
        # Get everything that the patient is asking to update
        keys = body.keys()
        __logger.info(f'Keys: {keys}')

        # Make sure a patient ID is provided to know which entry to upate
        dict_contains_item(body, 'patient_id')

        # Make sure only valid fields are trying to be updated
        if body is None or not set(keys).issubset(set(__updatable_information)):
            raise AssertionError(f'The contents of the request are invalid')

    except AssertionError as error:
        return format_return_message(400, str(error))

    # Invoke the update lambda to attempt to update the patient information
    response: dict = invoke_lambda(__patient_update_lambda_arn,
                                   __REQUEST_RESPONSE_INVOCATION_TYPE,
                                   event['body'])

    __logger.info(f'Update lambda returned: {response}')

    response_body: dict = json.loads(response['Payload'].read())
    return format_return_message(response_body['statusCode'], response_body['body'])


def delete_patient(event: dict) -> dict:
    """
    Validates a request to the delete endpoint, then deletes a patients' information from the database.

    :param event: The event that contains the patient id of the patient that is to be deleted.
    :return: JSON containing a status code, and a string message.
    """
    __logger.info(f'Invoked by the delete endpoint. Validating request.')

    body: dict = dict()
    if event['body'] is not None:
        body: dict = json.loads(event['body'])

    # Validate the information the patient passed
    try:
        dict_contains_item(body, 'patient_id')
    except AssertionError as error:
        return format_return_message(400, str(error))

    # Invoke the deletion lambda to attempt to delete the patient
    response: dict = invoke_lambda(__patient_deletion_lambda_arn,
                                   __REQUEST_RESPONSE_INVOCATION_TYPE,
                                   event['body'])
    __logger.info(f'Deletion lambda returned: {response}')

    # Parse the boto3 object to get the actual response payload
    response_body: dict = json.loads(response['Payload'].read())

    # Return a response to the patient, depending on what status code is returned
    if response_body['statusCode'] == 200:
        return format_return_message(200, f'The patient with the ID {response_body["body"]} was deleted successfully.')
    else:
        return format_return_message(response_body['statusCode'], response_body['body'])


def invoke_lambda(func_name: str, invocation_type: str, payload: Union[dict, str]) -> dict:
    """
    Invokes another lambda function using boto3.

    :param func_name: The name of the function to be invoked.
    :param invocation_type: The type of invocation. Will typically be RequestResponse.
    :param payload: The body of the request to the other lambda.
    :return: The dict that is returned from the invoked lambda
    """
    return __lambda.invoke(
        FunctionName=func_name,
        InvocationType=invocation_type,
        Payload=payload
    )


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


def validate_phone_number(number: str) -> None:
    """
    Uses a regex to ensure that a passed phone number is of a valid format.

    :param number: The phone number to be checked .
    :return: True if the phone number is valid, raise a ValueError if it is not.
    """
    if not __phone_regex.match(number):
        raise ValueError(f'The phone number entered is not in a valid format.')
