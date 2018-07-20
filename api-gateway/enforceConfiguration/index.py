import boto3
import json
import logging
import os
import sys

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('apigateway')

swagger_docs = []

authorizer_arn = os.environ['LAMBDA_AUTHORIZER_ARN']

def handler(event, context):
    logger.info('Verifying auth configuration for API Gateway endpoints')
    logger.info('Gathering information for all APIs')
    try:
        response = client.get_rest_apis()
    except Exception as e:
        logger.error(str(e))
        sys.exit(1)

    # Gather swagger docs for each stage of each API
    for endpoint in response['items']:
        id = endpoint['id']
        name = endpoint['name']

        logger.info('Gathering stage information for API {}'.format(name))
        try:
            stages = client.get_stages(
                restApiId=id
            )
        except Exception as e:
            logger.error(str(e))
            sys.exit(1)

        # Get the swagger export of each stage of the API
        for stage in stages['item']:
            logger.info('Exporting API definition for stage {} as swagger'.format(stage['stageName']))
            try:
                export_response = client.get_export(
                    restApiId=id,
                    stageName=stage['stageName'],
                    exportType='swagger'
                )
            except Exception as e:
                logger.error(str(e))
                sys.exit(1)

            swagger = json.loads(export_response['body'].read())
            swagger_docs.append(swagger)

    for doc in swagger_docs:
        # Make sure securityDefinitions is a key in the swagger document
        assert 'securityDefinitions' in doc, 'No securityDefinition present in swagger document for {} (Stage: {})'.format(
            doc['info']['title'],
            doc['basePath'][1:]
        )

        # Iterate through securityDefinitions to determine whether auth configuration is correct
        for definition in securityDefinitions:
            assert definition['x-amazon-apigateway-authtype'] is 'custom', 'authtype is not custom'
            assert definition['x-amazon-apigateway-authorizer']['type'] is 'token', 'authorizer is not of type token'
            assert definition['x-amazon-apigateway-authorizer']['authorizerUri'] is authorizer_arn, 'lambda authorizer is not correct'

    logger.info('All API Gateway endpoints configured with proper auth')
    return 'All API Gateway endpoints configured with proper auth'
