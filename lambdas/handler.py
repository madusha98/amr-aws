import json
import os

stage = os.environ.get("stage")

def hello(event, context):

    body = {
            "message": "Go Serverless v1.0! Your function executed successfully!",
            "stage": stage
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
