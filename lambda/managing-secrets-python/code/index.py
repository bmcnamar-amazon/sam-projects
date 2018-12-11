import json
import os
import sys
import boto3

client = boto3.client('secretsmanager')

secret_key = os.getenv('SECRET_KEY')

try:
    print('Trying to get the secret stored at the key {}'.format(secret_key))
    response = client.get_secret_value(
        SecretId=secret_key
    )
except Exception as e:
    print('Error: {}'.format(str(e)))
    sys.exit(1)


def handler(event, context):
    print('SecretString stored at {}: {}'.format(secret_key, response['SecretString']))
    secret = json.loads(response['SecretString'])
    return(secret['value'])
