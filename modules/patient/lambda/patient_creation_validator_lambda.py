import boto3
import logging
import json

lambda_client = boto3.client('lambda')

__logger = logging.getLogger()
__logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    __logger.info("This lambda was invoked with event: %s", event)

    response = lambda_client.invoke(
        FunctionName="arn:aws:lambda:us-west-2:146615276261:function:patient_creator_lambda",
        InvocationType="RequestResponse",
        Payload=json.dumps(event)
    )

    return response
