import counter_recognition
import json
import uuid
import time
import boto3
import base64
from botocore.config import Config
from decimal import Decimal
import os
import io
import simplejson as json

offline = os.environ.get("IS_OFFLINE")
stage = os.environ.get("stage")
bucket_name = 'meterimagesbucket-'+ stage

def read_digits(event, context):
  
  statusCode = 200

  value, image = counter_recognition.get_reading(event)
  try:
    if offline == "true":
      dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000', region_name='us-west-2')
      s3 = boto3.resource('s3', endpoint_url='http://localhost:4569', aws_access_key_id='S3RVER', aws_secret_access_key='S3RVER')
    else:
      dynamodb = boto3.resource('dynamodb')
      s3 = boto3.resource('s3')
      
    id = uuid.uuid4().hex
    value['readingId'] = id
    reading_value = value['value']
    
    image = image.convert('RGB')
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    
    image_name = id + '.jpg'
    s3.Object(bucket_name, image_name).put(Body=img_byte_arr)
    s3.ObjectAcl(bucket_name, image_name).put(ACL='public-read')
    
    url = f'https://{bucket_name}.s3.amazonaws.com/{image_name}'
    
    
    item = {
      "readingId": id,
      "value": reading_value,
      "score": Decimal(str(value['score'])),
      "date": Decimal(str(time.time())),
      "accId": event["queryStringParameters"]['accId'],
      "imageUrl": url
    }
    table = dynamodb.Table('monthlyReadingTable-' + stage)
    resp = table.put_item(Item=item)
    print(resp)

    
    
  except Exception as e:
    print(e)
    statusCode = 500

  return {
    'statusCode': statusCode,
    'body': json.dumps(value, use_decimal=True)
  }