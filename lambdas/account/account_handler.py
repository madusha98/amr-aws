import json
import boto3
import base64
from botocore.config import Config


def add_account(event, context):
    statusCode = 200
    responseBody = {'data': ''}
    dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000', region_name='us-west-2') # local
    # dynamodb = boto3.resource('dynamodb')
    # body_dec = base64.b64decode(event['body'])
    # req = json.loads(body_dec)
    # To run locally
    req = json.loads(event['body'])
    try:
        print(req['accId'])
        # input data to database
        table = dynamodb.Table('accountTable')
        resp = table.put_item(Item={
            'accId': req['accId'],
            'userId': req['userId'],
            'accNo': req['accNo'],
            'outstanding': req['outstanding'],
            'location': req['location']
        })
        responseBody = {"data": resp, "message": "Account added successfully"}
# error handling
    except Exception as e:
        print('Exception: ', e)
        statusCode = 500
        responseBody = {"error": str(e)}
# response
    response = {
        "statusCode": statusCode,
        "body": json.dumps(responseBody)
    }

    return response
