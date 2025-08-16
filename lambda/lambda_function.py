import os
import boto3
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import uuid
import json
import datetime

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    dynamodb = boto3.resource('dynamodb')
    processed_bucket = os.environ['PROCESSED_BUCKET']
    metadata_table = dynamodb.Table(os.environ['METADATA_TABLE'])

    # API Gateway trigger
    if 'httpMethod' in event:
        if event['httpMethod'] == 'POST' and event.get('body'):
            body = json.loads(event['body'])
            image_data = base64.b64decode(body['image'])
            key = f"{uuid.uuid4()}.jpg"
            
            process_and_upload(s3, image_data, processed_bucket, key)
            
            metadata_table.put_item(Item={
                'image_id': key,
                'timestamp': datetime.datetime.utcnow().isoformat(),
                'source': 'api'
            })
            
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Image uploaded and processed.', 'key': key})
            }

    # S3 trigger
    elif 'Records' in event:
        for record in event['Records']:
            src_bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']
            
            img_obj = s3.get_object(Bucket=src_bucket, Key=key)
            img_data = img_obj['Body'].read()
            
            process_and_upload(s3, img_data, processed_bucket, key)

            metadata_table.put_item(Item={
                'image_id': key,
                'timestamp': datetime.datetime.utcnow().isoformat(),
                'source': 's3'
            })

    return {'statusCode': 200, 'body': 'Image processed.'}

def process_and_upload(s3, img_data, processed_bucket, key):
    img = Image.open(io.BytesIO(img_data))
    img = img.resize((512, 512))
    watermark_text = "Sample"
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    draw.text((10, 10), watermark_text, (255, 255, 255), font=font)
    buffer = io.BytesIO()
    img.save(buffer, 'JPEG')
    buffer.seek(0)
    s3.put_object(Bucket=processed_bucket, Key=key, Body=buffer, ContentType='image/jpeg')
