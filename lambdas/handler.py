import simplejson as json
import boto3


def hello(event, context):
    dynamodb = boto3.resource('dynamodb')
    # dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000', region_name='us-west-2') # local
    try:
        table = dynamodb.Table('monthlyReadingTable')
        # item = table.get_item(Key={'accId': 'abc'})
        # print(item)
        response = table.scan()
        items = response['Items']
        print(items)
        body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "data": items
        }

    except Exception as e:
        print('Exception: ', e)


    response = {
        "statusCode": 200,
        "body": json.dumps(body, use_decimal=True)
    }

    return response
