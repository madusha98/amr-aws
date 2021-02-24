import json
import boto3


def update_token(event, context):
    statusCode = 200
    responseBody = {'data': ''}
    dynamodb = boto3.resource('dynamodb')

    req = json.loads(event['body'])
    try:
        table = dynamodb.Table('devicesTable')
        item = table.get_item(Key={'deviceId': req['deviceId']})
        print('Item', item)
        if ('Item' not in item):
            resp = table.put_item(Item={
                'deviceId': req['deviceId'],
                'pushToken': req['pushToken']
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