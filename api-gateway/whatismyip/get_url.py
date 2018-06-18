import boto3
import sys

# The purpose of this script is to determine the URL of the newly created
# API Gateway endpoint

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
        results = cf_client.describe_stacks(StackName=stack_name)
    except Exception as e:
        print 'Error: Could not describe stacks for {}: {}'.format(stack_name, str(e))
        sys.exit(1)

    print results['Stacks'][0]['Outputs'][0]['OutputValue']

if __name__ == '__main__':
    main()
