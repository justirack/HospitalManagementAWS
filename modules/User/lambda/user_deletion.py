def lambda_handler(event: dict, context: dict) -> dict:
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html; charset=utf-8"},
        "body": "Success"

    }