import boto3
import sys

# The purpose of this script is to identify Kinesis stream(s) generated
# by SAM / CloudFormation.

streams = []

def usage(msg):
    print '{} <YOUR STACK NAME>'.format(sys.argv[0])
    print 'Error: {}'.format(msg)
    sys.exit(1)

def main():

    if len(sys.argv) != 2:
        usage('Please supply the stack name')

    stack_name = sys.argv[1]

    try:
        cf_client = boto3.client('cloudformation')
    except Exception as e:
        print 'Error: Could not create Cloudformation client object: {}'.format(str(e))
        sys.exit(1)

    try:
        results = cf_client.list_stack_resources(StackName=stack_name)
    except Exception as e:
        print 'Error: Could not get list stack resources for {}: {}'.format(stack_name, str(e))

    for resource in results['StackResourceSummaries']:
        if resource['ResourceType'] == 'AWS::Kinesis::Stream':
            streams.append(resource['PhysicalResourceId'])

    for stream in streams:
        print stream

if __name__ == '__main__':
    main()
