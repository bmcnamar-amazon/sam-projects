import base64
import boto3
import hashlib
import json
import logging
import os
import sys


logger = logging.getLogger()
logger.setLevel(logging.INFO)


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.getenv('SCORES_TABLE'))


def handler(event=None, context=None):
    records = []

    # Get data from Kinesis stream to put to DynamoDB
    for record in event['Records']:
        payload = base64.b64decode(record['kinesis']['data'])
        logger.info('Decoded payload: {}'.format(payload))
        
        # Payload is of type string. Converting to json
        json_payload = json.loads(payload)

        # Generate md5sum of the payload. Make this the value for the json_payload key 'id'.
        payload_md5 = hashlib.md5(payload).hexdigest()
        json_payload['id'] = payload_md5

        try:
            result = table.put_item(Item=json_payload)
        except Exception as e:
            logger.error('Could not insert payload into {} table: {}'.format(os.getenv('SCORES_TABLE'), str(e)))
            sys.exit(1)
        
        logger.info('Successfully inserted {} to {} table'.format(json_payload, os.getenv('SCORES_TABLE')))
        records.append(result)
    
    logger.info('Successfully processed {} records'.format(len(records)))
    return len(records)
