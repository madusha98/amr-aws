import counter_recognition
import json
import uuid
import time
import boto3
import base64
from botocore.config import Config
from decimal import Decimal
import os

offline = os.environ.get("IS_OFFLINE")
stage = os.environ.get("stage")

def read_digits(event, context):

  value, image = counter_recognition.get_reading(event)
  try:
    if offline == "true":
      dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000', region_name='us-west-2')
      s3 = boto3.resource('s3', endpoint_url='http://localhost:4569', aws_access_key_id='S3RVER', aws_secret_access_key='S3RVER')
    else:
      dynamodb = boto3.resource('dynamodb')
      s3 = boto3.resource('s3')
    id = uuid.uuid4().hex
    item = {
      "readingId": id,
      "value": value['value'],
      "score": Decimal(str(value['score'])),
      "date": Decimal(str(time.time())),
      "accId": event["queryStringParameters"]['accId'],
      "imageUrl": "google.lk"
    }
    table = dynamodb.Table('monthlyReadingTable-' + stage)
    resp = table.put_item(Item=item)
    print(resp)

    s3.Object('MeterImagesBucket-'+ stage, id + '.jpg').put(Body=image)
  except Exception as e:
    print(e)

  return {
    'statusCode': 200,
    'body': json.dumps(value)
  }
