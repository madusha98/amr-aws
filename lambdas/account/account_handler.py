import json
import boto3
import base64
from botocore.config import Config
import os
from boto3.dynamodb.conditions import Key, Attr
import uuid
import time
from decimal import Decimal

offline = os.environ.get("IS_OFFLINE")
stage = os.environ.get("stage")

def add_account(event, context):
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
            
        # input data to database
        table = dynamodb.Table('accountTable-' + stage)

        alreadyExists = table.scan(
            FilterExpression=Attr('userId').eq(req['userId'])
        )

        if (len(alreadyExists['Items']) > 0):
            deleted = table.delete_item(Key={'accId':alreadyExists['Items'][0]['accId']})
            print(deleted)
        id = uuid.uuid4().hex
        resp = table.put_item(Item={
            'accId': id,
            'userId': req['userId'],
            'accNo': req['accNo'],
            'outstanding': req['outstanding'],
            'location': req['location'],
            "date": Decimal(str(time.time()))
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
