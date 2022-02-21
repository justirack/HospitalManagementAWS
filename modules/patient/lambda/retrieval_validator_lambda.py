import boto3
import json
import os
import logging

__PATIENT_RETRIEVER_LAMBDA_ARN = os.getenv('PATIENT_RETRIEVER_LAMBDA_ARN')

lambda_client = boto3.client('lambda')

__logger = logging.getLogger()
__logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    pass
