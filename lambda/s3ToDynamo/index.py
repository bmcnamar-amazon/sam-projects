import boto3
import json
from pprint import pprint
import sys
import uuid

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('tickers')

bucket_keyspace = 's3ToDynamo'

local_directory = '/tmp'

def handler(event, context):
    # Extract out S3 object details
    s3_dict = event['Records'][0]['s3']
    bucket = s3_dict['bucket']['name']
    key = s3_dict['object']['key']
    object_name = key.split('/')[-1]
    local_file = local_directory + '/' + object_name
    

    # Copy S3 object locally to /tmp
    print 'Copying s3://{}/{} to {}...'.format(bucket, key, local_file)
    try:
        s3.Bucket(bucket).download_file(key, '{}'.format(local_file))
    except Exception as e:
        print 'ERROR: Failed to copy s3://{}/{} to {}: {}'.format(bucket, key, local_file, str(e))
        sys.exit(1)

    # Take in entries from JSON file
    try:
        data = json.load(open('{}'.format(local_file)))
    except:
        print 'ERROR: Failed to open {}: {}'.format(local_file, str(e))
        sys.exit(1)

    # Set values accordingly
    id = str(uuid.uuid4())
    exchange = data['exchange']
    ticker = data['ticker']
    time = data['time']
    price = int(data['price'] * 100)
    currency = data['currency']

    # Insert values into DynamoDB table
    try:
        table.put_item(
            Item={
                'id': id,
                'exchange': exchange,
                'ticker': ticker,
                'time': time,
                'price': price,
                'currency': currency
            }
        )
    except Exception as e:
        print 'ERROR: Failed to insert ticker to tickers DynamoDB table: {}'.format(str(e))
        sys.exit(1)
    
    print 'Inserted record to tickers DynamoDB table'
    return 'SUCCESS: Extracted data from JSON document in s3://{}/{} to ticker DynamoDB table'.format(bucket, key)
