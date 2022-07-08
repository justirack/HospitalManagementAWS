import boto3
import logging
import os
import uuid

__DYNAMO_DB_TABLE_NAME = os.getenv('PATIENT_TABLE_NAME')

__dynamodb = boto3.client('dynamodb')

__logger = logging.getLogger()
__logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    __logger.info(f"This lambda was invoked with event: {event}")

    # patient_id = str(uuid.uuid4())
    # sort_key = event['first_name'][0] + event['last_name'][0] + event['date_of_birth']
    #
    # response = __dynamodb.put_item(
    #     TableName=__DYNAMO_DB_TABLE_NAME,
    #     Item={
    #         "patient_id": {'S': patient_id},
    #         'sort_key': {'S': sort_key},
    #         'first_name': {'S': event['first_name']},
    #         'last_name': {'S': event['last_name']},
    #         "date_of_birth": {'S': event['date_of_birth']}
    #     }
    # )
    # __logger.info(f"Received response: {response}")
    #
    # # Add the patient id to the response if the add was successful
    # if response['ResponseMetadata']['HTTPStatusCode'] == 200:
    #     response.update({
    #         'patient_id': patient_id
    #     })
    #
    # return response




# Received record:
# {
#     "Records": [
#         {
#             "messageId": "7110e211-c62f-4aff-8044-9b7e75b03f21",
#             "receiptHandle": "AQEByWazHXsjWO8XLb0zVwVXvOsVBkhTFQEFmCNgdQm5dWADu2PevG0qVhNZ4+Y+mb2kJn/4WqPZdv3eiJkY3z/NYeEy+qtzAgHZB5RwW5Lx3ZSmACDM0mDEyS08C0HD2fw1c+4aMoIOdgqfY3SZvwwRFqujoVsCclfyLBZCO9QQQjUGf0QofMv2Uav+EmCkhxGIivb2HcxLXnAtYMnfqzW0vSpLJrloWtRzWKBL+GfXqIE6nyBtG/H75QHahhni79dY1fr8ziRZMc2NZz/kntoY3MFiT5W52deg0Ok4Ejbv0BgvqQ497LCoJlzUjfHA+OaAUG+cg8g1qGzvlIXqRGcoGXCaaqjk/+IU526qgxmbDkrK/BYOdXo41ePep8xPI2P3ry5zdXzgRTNt06f0KnCa/1BMbl3bZ/J5eqr3NNYiEzc=",
#             "body": "{\"first_name\": \"Justin\", \"last_name\": \"Rackley\", \"date_of_birth\": \"2002-02-09\"}",
#             "attributes": {
#                 "ApproximateReceiveCount": "1",
#                 "SentTimestamp": "1657283547731",
#                 "SenderId": "AROASEIXTSLSZY3HRM6KE:patient-patient_validator",
#                 "ApproximateFirstReceiveTimestamp": "1657283547743"
#             },
#             "messageAttributes": {
#
#             },
#             "md5OfMessageAttributes": "None",
#             "md5OfBody": "7ed594e5565f27a53d71869d5fe701a7",
#             "eventSource": "aws:sqs",
#             "eventSourceARN": "arn:aws:sqs:us-west-2:146615276261:patient-create_patient_queue",
#             "awsRegion": "us-west-2"
#         }
#     ]
# }