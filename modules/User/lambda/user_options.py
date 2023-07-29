import json


def lambda_handler(event: dict, context: dict):
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Accept, Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS'
        },
        'body': json.dumps('Hello from Lambda!')
    }