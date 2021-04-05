import simplejson as json
import base64
import boto3
from boto3.dynamodb.conditions import Key, Attr
import os

offline = os.environ.get("IS_OFFLINE")

def get_history(event, context):

    statusCode = 200

    try:
        if offline == "true":
            dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000', region_name='us-west-2')
        else:
            dynamodb = boto3.resource('dynamodb')

        table = dynamodb.Table('billTable')
        response = table.scan(
            # ProjectionExpression="billValue",
            FilterExpression=Attr('accId').eq(event["queryStringParameters"]['accId'])
        )
        data = []
        print(response)
        for res in response['Items']:
            # print(json.dumps(res))
            item = {
                "billValue": res['billValue'],
                "date": res['date'],
                "billId": res['billId']
            }
            print(res)
            data.append(item)
        responseBody=json.dumps(data, use_decimal=True)
    except Exception as e:
        print('Exception: ', e)
        statusCode = 500
        responseBody = {"error": str(e)}

    responseJson = {
        "statusCode": statusCode,
        "body": responseBody
    }

    return responseJson
