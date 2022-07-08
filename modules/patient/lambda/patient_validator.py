import logging

__logger = logging.getLogger()
__logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    __logger.info(f'Lambda was invoked with: {event}')
