import boto3
import logging

lambda_client = boto3.client('lambda')

__logger = logging.getLogger()
__logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    __logger.info("This lambda was invoked with event: %s", event)

    response = lambda_client.invoke(
        FunctionName="",
        InvocationType="",
        Payload=event
    )

    return response
