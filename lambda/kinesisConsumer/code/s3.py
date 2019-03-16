import base64
import boto3
import hashlib
import json
import logging
import os
import sys


logger = logging.getLogger()
logger.setLevel(logging.INFO)


s3 = boto3.client('s3')
output_bucket = os.environ['SCORES_BUCKET']


def handler(event=None, context=None):
    records = []

    # Get data from Kinesis stream to put to DynamoDB
    for record in event['Records']:
        payload = base64.b64decode(record['kinesis']['data'])
        logger.info('Decoded payload: {}'.format(payload))

        # Generate md5sum of the payload. Make this the object name.
        payload_md5 = hashlib.md5(payload).hexdigest()

        try:
            result = s3.put_object(Bucket=output_bucket,
                Key=payload_md5,
                Body=payload
            )
        except Exception as e:
            logger.error('Could not put object to {} bucket: {}'.format(output_bucket, str(e)))
            sys.exit(1)
        
        logger.info('Successfully put object to to {} bucket'.format(output_bucket))
        records.append(result)
    
    logger.info('Successfully processed {} records'.format(len(records)))
    return len(records)
