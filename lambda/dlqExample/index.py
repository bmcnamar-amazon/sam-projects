import boto3
import os
import time

s3 = boto3.resource('s3')

# output_bucket = os.environ['OUTPUT_BUCKET']

def handler(event, context):
    input_bucket = event['Records'][0]['s3']['bucket']['name']
    input_file = event['Records'][0]['s3']['object']['key']

    try:
        print 'Sleeping for longer than the function can run...'
        time.sleep(30)
        s3.Bucket(input_bucket).download_file(input_file, '/tmp/{}'.format(input_file))
    except Exception as e:
        print 'Error: {}'.format(str(e))
        sys.exit(1)

    print 'Should never print to logs because the Lambda service will kill the function'
    return 'Should never print to logs because the Lambda service will kill the function'