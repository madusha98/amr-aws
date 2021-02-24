import json
import boto3


def update_token(event, context):
    statusCode = 200
    responseBody = {'data': ''}
    dynamodb = boto3.client('dynamodb')

    params = {
        'TableName': 'devicesTable',
        'Key': {
            'deviceId': '123',
            'pushToken': 'afdafdfa'
        },
        'UpdateExpression': 'SET isActive = :isActiveVal',
        'ConditionExpression': 'attribute_exists(deviceId)',
        'ExpressionAttributeValues': {
            ':isActiveVal': 'false'
            },
        'ReturnValues': "ALL_NEW"
    }
    try:
        resp = dynamodb.put_item(params)
        responseBody = { "data": resp }

    except Exception as e:
        print('Exception: ', e)
        statusCode = 500
        responseBody = {"error": e }

    response = {
        "statusCode": statusCode,
        "body": json.dumps(responseBody)
    }

    return response