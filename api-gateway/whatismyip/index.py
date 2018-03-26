def handler(event, context):
    print 'Requester IP: {}'.format(event['myip'])
    return event['myip']