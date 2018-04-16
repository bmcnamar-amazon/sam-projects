def handler(event, context):
    print 'Version: {}'.format(context.function_version)
    print 'ARN: {}'.format(context.invoked_function_arn)
    return 'Version: {}  ARN: {}'.format(context.function_version, context.invoked_function_arn)