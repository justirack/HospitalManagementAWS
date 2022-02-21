import boto3
import json
import os
import logging

__DYNAMO_DB_TABLE_NAME = os.getenv('PATIENT_TABLE_NAME')

dynamodb = boto3.client('dynamodb')

__logger = logging.getLogger()
__logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    pass
