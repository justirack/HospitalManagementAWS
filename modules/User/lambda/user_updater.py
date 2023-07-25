import re
import logging
import datetime

__logger = logging.getLogger()
__logger.setLevel(logging.INFO)

__regex = "^(([0-9]{10})|\([0-9]{3}\)(|\s)[0-9]{3}-[0-9]{4}|[0-9]{3}-[0-9]{3}-[0-9]{4}|[0-9]{3}\s[0-9]{3}\s[0-9]{4})$"

def lambda_handler(event, context):
    __logger.info(f'date: {event["date"]}')

    try:
        datetime.date.fromisoformat(event['date'])
        __logger.info("The format is correct")
    except ValueError:
        __logger.info("Incorrect format")

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html; charset=utf-8"},
        "body": "Success"

    }