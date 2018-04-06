from pprint import pprint

def handler(event, context):
    info = {}
    
    base = event['Records'][0]['Sns']
    info['error_message'] = base['MessageAttributes']['ErrorMessage']['Value']
    info['request_id'] = base['MessageAttributes']['RequestID']['Value']
    info['topic_arn'] = base['TopicArn']
    
    pprint(info)
    return(info)