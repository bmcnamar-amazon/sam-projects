import base64
import boto3
import json
import logging
import os
from pymongo import MongoClient
import sys
import urllib

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ssm_config_path = '/' + os.getenv('SSM_CONFIG_NAME') + '/'
database_name = os.getenv('MONGO_DATABASE', 'example_db')
# collection = 'scores'

ssm_client = boto3.client('ssm')


def load_config(ssm_parameter_path):
    try:
        param_details = ssm_client.get_parameters_by_path(
            Path=ssm_parameter_path,
            Recursive=False,
            WithDecryption=True
        )

        config_dict = {}
    
        # Loop through the returned parameters and populate config_dict
        if 'Parameters' in param_details and len(param_details.get('Parameters')) > 0:
            for param in param_details.get('Parameters'):
                param_key = param.get('Name').split("/")[-1]
                param_value = param.get('Value')
                config_dict[param_key] = param_value

    except Exception as e:
        logger.error(str(e))
    finally:
        return config_dict


def put_data(event, context):
    config = load_config(ssm_config_path)

    mongo_hostname = config['hostname']
    mongo_user = urllib.quote_plus(config['username'])
    mongo_password = urllib.quote_plus(config['password'])

    try:
        logger.info('Connecting to MongoDB {}'.format(mongo_hostname))
        connection_string = 'mongodb+srv://{}:{}@{}/{}?authMechanism=SCRAM-SHA-1'.format(mongo_user, mongo_password, mongo_hostname, database_name)
        
        try:
            mongo_client = MongoClient(connection_string)
        except Exception as e:
            logger.error('Could not connect to {}: {}'.format(database_name, str(e)))
    except Exception as e:
        logger.error(str(e))
    
    records = []

    # Get data from Kinesis stream to put to MongoDB
    for record in event['Records']:
        payload = base64.b64decode(record['kinesis']['data'])
        logger.info('Decoded payload: {}'.format(payload))
        
        # payload is of type string. converting to json
        json_payload = json.loads(payload)

        db = mongo_client[database_name]
        collection = db['scores']

        try:
            result = collection.insert_one(json_payload)
        except Exception as e:
            logger.error('Could not insert payload into scores collection: {}'.format(str(e)))
            sys.exit(1)
        
        logger.info('Successfully inserted {} to scores collection'.format(json_payload))
        records.append(result)
    
    logger.info('Successfully processed {} records'.format(len(records)))
    return len(records)

def get_data(event, context):
    config = load_config(ssm_config_path)
    query = event['query']

    mongo_hostname = config['hostname']
    mongo_user = urllib.quote_plus(config['username'])
    mongo_password = urllib.quote_plus(config['password'])

    logger.info('Connecting to MongoDB {}'.format(mongo_hostname))
    connection_string = 'mongodb+srv://{}:{}@{}/{}?authMechanism=SCRAM-SHA-1'.format(mongo_user, mongo_password, mongo_hostname, database_name)
    
    try:
        mongo_client = MongoClient(connection_string)
    except Exception as e:
        logger.error('Could not connect to {}: {}'.format(database_name, str(e)))
    
    db = mongo_client[database_name]
    collection = db['scores']

    try:
        results = collection.find(query)
    except Exception as e:
        logger.error('Could not execute query against the scores collection: {}'.format(str(e)))
        sys.exit(1)
    
    logger.info('Found {} results from query {}'.format(len(results), query))
    for result in results:
        logger.info(result)
    
    return len(results)

    