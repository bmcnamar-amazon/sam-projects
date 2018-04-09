import boto3 
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all 

patch_all()

s3 = boto3.resource('s3')

local_directory = '/tmp'

def handler(event, context):

    # Extract out S3 object details
    valid_bucket = event['valid_bucket_name']
    valid_key = event['valid_key']
    nonexistent_bucket = event['nonexistent_bucket']
    nonexistent_key = event['nonexistent_key']

    # Create a segment
    xray_recorder.begin_segment('s3trace')

    # Copy valid S3 object locally to /tmp
    valid_subsegment = xray_recorder.begin_subsegment('valid')
    local_file = local_directory + '/' + valid_key
    print 'Copying valid object s3://{}/{} to {}...'.format(valid_bucket, valid_key, local_file)
    try:
        s3.Bucket(valid_bucket).download_file(valid_key, '{}'.format(local_file))
    except Exception as e:
        print 'Error: {}'.format(str(e))
    xray_recorder.end_subsegment()

    # Copy invalid S3 object locally to /tmp
    invalid_subsegment = xray_recorder.begin_segment('invalid')
    local_file = local_directory + '/' + nonexistent_key
    print 'Copying invalid object s3://{}/{} to {}...'.format(nonexistent_bucket, nonexistent_key, local_file)
    try:
        s3.Bucket(nonexistent_bucket).download_file(nonexistent_key, '{}'.format(local_file))
    except Exception as e:
        print 'Error: {}'.format(str(e))
    xray_recorder.end_subsegment()

    # End segment
    xray_recorder.end_segment()
    return '{"message": "X-Ray worked"}'