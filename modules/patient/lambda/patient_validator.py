import os
import json
import boto3
import logging

__logger = logging.getLogger()
__logger.setLevel(logging.INFO)

__CREATE_PATIENT_QUEUE_URL = os.getenv('CREATE_PATIENT_QUEUE_URL')


def lambda_handler(event, context):
    __logger.info(f'Lambda was invoked with: {event}')

    return {
        "statusCode": 200,
        "headers": {
            'Content-Type': 'text/html; charset=utf-8'
        },
        "body": json.dumps({
            "message": "Success"
        })

    }
