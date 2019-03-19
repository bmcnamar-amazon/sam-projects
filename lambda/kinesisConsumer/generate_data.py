import boto3
from datetime import datetime
import json
import random
import sys
import time


client = boto3.client('kinesis')

try:
    stream_name = sys.argv[1]
except Exception as e:
    print 'Error: Need to pass in name of Kinesis stream'
    sys.exit(1)

partition_key = 'gamers'

first_names = ['Chris', 'George', 'Stefano', 'Jim', 'Dottie', 'Matt', 'Ellie', 'Lia', 'Adam']
last_names = ['Smith', 'Jones', 'Mao', 'Ballew', 'Johnson', 'Singh', 'Brayley-Berger', 'Wagner', 'Lee', 'Feng', 'Richardson']
ip_addresses = ['52.24.107.12', '53.42.10.8', '204.12.18.9', '88.44.22.11', '77.9.83.10', '9.9.12.10', '20.43.10.83', '17.12.33.30', '12.92.8.2', '176.1.38.90', '230.229.228.7', '140.92.75.150']


def put_to_stream(firstname, lastname, score, ip_address, timestamp):
    payload = {
        'firstname': firstname,
        'lastname': lastname,
        'score': score,
        'ip_address': ip_address,
        'timestamp': timestamp
    }

    print payload

    try:
        put_response = client.put_record(
                            StreamName=stream_name,
                            Data=json.dumps(payload),
                            PartitionKey=partition_key)
    except Exception as e:
        print 'Error: {}'.format(e)
        sys.exit(1)

    return put_response


while True:
    firstname = random.choice(first_names)
    lastname = random.choice(last_names)
    score = int(random.random() * 100)
    ip_address = random.choice(ip_addresses)
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    result = put_to_stream(firstname, lastname, score, ip_address, timestamp)
    print result
    print
    time.sleep(5)
