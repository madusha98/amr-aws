import json
import base64
import boto3
from boto3.dynamodb.conditions import Key, Attr


def get_history(event, context):
    statusCode = 200
    dynamodb = boto3.resource('dynamodb')
    body_dec = base64.b64decode(event['body'])
    req = json.loads(body_dec) 
    # req = json.loads(event['body']) # Uncomment to run locally
    try:
        table = dynamodb.Table('billTable')
        response = table.scan(
            ProjectionExpression="billValue",
            FilterExpression=Attr('accId').eq(req['accId'])
        )
        data = []
        for res in response['Items']:
            # print(json.dumps(res))
            item = {"billValue": res['billValue']['Total']}
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
