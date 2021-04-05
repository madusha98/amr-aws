import json
import base64
import boto3
from boto3.dynamodb.conditions import Key, Attr
import os

offline = os.environ.get("IS_OFFLINE")

def get_meter_history(event, context):
    statusCode = 200
    dynamodb = boto3.resource('dynamodb')

    try:
        if offline == "true":
            dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000', region_name='us-west-2')
        else:
            dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('monthlyReadingTable')
        response = table.scan(
            ProjectionExpression="readingId",
            FilterExpression=Attr('accId').eq(event["queryStringParameters"]['accId'])
        )
        data = []
        for res in response['Items']:
            # print(json.dumps(res))
            item = {
                "readingId": res[id],
                "value": res['value'],
                "score": res['score'],
                "date": res["date"],
                "imageUrl": res["imagUrl"]
            }
            # print(item)
            data.append(item)
        responseBody=json.dumps(data)
    except Exception as e:
        print('Exception: ', e)
        statusCode = 500
        responseBody = {"error": str(e)}

    responseJson = {
        "statusCode": statusCode,
        "body": responseBody
    }

    return responseJson
