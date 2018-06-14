import boto3
import sys
import time

try:
    stream_name = sys.argv[1]
except Exception as e:
    print 'Error: Need to pass in name of Kinesis stream'
    sys.exit(1)

client = boto3.client('kinesis')

response = client.describe_stream(StreamName=stream_name)
print 'DEBUG describe_stream response: {}'.format(response)

shard_id = response['StreamDescription']['Shards'][0]['ShardId']
print 'DEBUG shard_id: {}'.format(shard_id)

shard_iterator = client.get_shard_iterator(StreamName=stream_name,
                                                    ShardId=shard_id,
                                                    ShardIteratorType='LATEST')

shard_iterator = shard_iterator['ShardIterator']
print 'DEBUG shard_iterator: {}'.format(shard_iterator)

record_response = client.get_records(ShardIterator=shard_iterator,
                                              Limit=10)
print 'DEBUG record_response: {}'.format(record_response)

while 'NextShardIterator' in record_response:
    response = client.get_records(ShardIterator=record_response['NextShardIterator'],
                                                  Limit=10)
    for record in response['Records']:
        print record['Data']
    # print response['Records']
    print
    # wait for 5 seconds
    time.sleep(5)