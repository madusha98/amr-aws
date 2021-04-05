import json
import boto3
import base64
from botocore.config import Config
import os

offline = os.environ.get("IS_OFFLINE")

def update_token(event, context):
    statusCode = 200
    responseBody = {'data': ''}

    try:
        if offline == "true":
            dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000', region_name='us-west-2')
            req = json.loads(event['body'])
        else:
            dynamodb = boto3.resource('dynamodb')
            body_dec = base64.b64decode(event['body'])
            req = json.loads(body_dec)
        table = dynamodb.Table('devicesTable')
        item = table.get_item(Key={'deviceId': req['deviceId']})
        print('Item', item)
        if ('Item' not in item):
            resp = table.put_item(Item={
                'deviceId': req['deviceId'],
                'pushToken': req['pushToken'],
                'userId': req['userId']
            })
            responseBody = { "data": resp, "message": "Added Successfully" }
        else:
            resp = table.update_item(Key={
            'deviceId': req['deviceId']
            },
            UpdateExpression='SET pushToken = :pushToken',
                ExpressionAttributeValues={
                ':pushToken': req['pushToken']
            })
            responseBody = { "data": resp, "message": "Updated Successfully" }
    except Exception as e:
        print('Exception: ', e)
        statusCode = 500
        responseBody = {"error": str(e) }

    response = {
        "statusCode": statusCode,
        "body": json.dumps(responseBody)
    }

    return response