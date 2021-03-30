import json
import boto3


def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!"
    }
    # dynamodb = boto3.resource('dynamodb')
    # try:
    #     table = dynamodb.Table('billTable')
    #     item = table.get_item(Key={'accId': 'abc'})
    #     print(item)

    # except Exception as e:
    #     print('Exception: ', e)


    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
