import boto3
import sys

# The purpose of this script is to remove the contents of the bucket generated
# by SAM / CloudFormation.  Cloudformation cannot remove buckets that have
# contents.

generated_buckets = []

def usage(msg):
    print 'Error: {}'.format(msg)
    sys.exit(1)

def main():

    if len(sys.argv) != 2:
        usage('Please  supply the name of a single Cloudformation stack')

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
        if resource['ResourceType'] == 'AWS::S3::Bucket':
            generated_buckets.append(resource['PhysicalResourceId'])

    try:
        s3_resource = boto3.resource('s3')
    except Exception as e:
        print 'Error: Could not create S3 client object: {}'.format(str(e))
        sys.exit(1)



    for bucket in generated_buckets:
        try:
            b = s3_resource.Bucket(bucket)
        except:
            print 'Error: {}'.str(e)
            sys.exit(1)
        print 'Removing contents of {}...'.format(bucket)
        try:
            b.objects.all().delete()
        except:
            print 'Error: {}'.str(e)
            sys.exit(1)




if __name__ == '__main__':
    main()
