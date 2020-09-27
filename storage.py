import boto3
from botocore.config import Config
from decouple import config

s3_client = None

def create_client():
  return boto3.client('s3',
    aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
    region_name=config('AWS_DEFAULT_REGION')
  )

def put_image(resource_key, data):
  s3_client.put_object(
    ACL='public-read',
    Bucket=config('S3_BUCKET'),
    Key=f'user-content/{resource_key}', 
    Body=data,
    ContentType='image/jpeg'
  )

def init():
  global s3_client
  s3_client = create_client()