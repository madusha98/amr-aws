import json
import base64
import boto3
from boto3.dynamodb.conditions import Key, Attr
import os
import simplejson as json

offline = os.environ.get("IS_OFFLINE")
stage = os.environ.get("stage")

def get_account_detaills(event, context):
    statusCode = 200
    dynamodb = boto3.resource('dynamodb')

    try:
        if offline == "true":
            dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000', region_name='us-west-2')
        else:
            dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('accountTable-' + stage)
        response = table.scan(
            FilterExpression=Attr('userId').eq(event["queryStringParameters"]['userId'])
        )
        print(response)
        responseBody=json.dumps(response['Items'], use_decimal=True)
    except Exception as e:
        print('Exception: ', e)
        statusCode = 500
        responseBody = {"error": str(e)}

    responseJson = {
        "statusCode": statusCode,
        "body": responseBody
    }

    return responseJson