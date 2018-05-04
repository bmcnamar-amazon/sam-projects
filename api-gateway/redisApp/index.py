import json
import logging
import os
import redis

logger = logging.getLogger()
logger.setLevel(logging.INFO)

redis_endpoint = os.getenv('REDIS_URL') # hostname:port
redis_host, redis_port = redis_endpoint.split(':')
r = redis.Redis(host=redis_host, port=redis_port, db=0)

def get(event, context):
    _key = event['pathParameters']['username']

    try:
        result = r.hgetall('user:{}'.format(_key))
        logger.info('Queried value for user:{} {}'.format(_key, result))
        return {"body": json.dumps(result), "statusCode": 200}
    except Exception as e:
        logger.error('Exception occurred: {}'.format(str(e)))
        return {"body": "fail", "statusCode": 500}

def post(event, context):
    _key = event['pathParameters']['username']

    if event['body'] != '':
        body = json.loads(event['body'])
        name = body['name']
        email = body['email']
        data = {"name": name, "email": email}
        
        try:
            result = r.hmset('user:' + _key, data)
            logger.info('Created entry for {}: {}'.format(name, data))
            return {"body": "ok", "statusCode": 200}
        except Exception as e:
            logger.error('Exception occurred: {}'.format(str(e)))
            return {"body": "fail", "statusCode": 500}
    else:
        return {"body": "need to pass in name and email as a dictionary", "statusCode": 500}

    