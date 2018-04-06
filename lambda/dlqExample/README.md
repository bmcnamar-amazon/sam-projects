# dlqExample

This example will deploy a function that will intentionally fail and write data to a [Dead Letter Queue](https://docs.aws.amazon.com/lambda/latest/dg/dlq.html) - abbreviated DLQ.  It is important to remember that unprocessed events are sent to a DLQ when invoked asynchronously.  

DLQ directs unprocessed events to a [Amazon SQS queue](http://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/Welcome.html) or [Amazon SNS topic](http://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/Welcome.html).  The code in this example sends data to a SNS topic.

# Locally Test Function to Parse SNS Notification

```
sam local invoke snsHandlerFunction -e event.json
```

# Deploy Function to AWS

## Package the Function

```
sam package --template-file template.yml \
--output-template-file packaged-template.yml \
--s3-bucket <YOUR S3 BUCKET>
```

eg.

```
sam package --template-file template.yml \
--output-template-file packaged-template.yml \
--s3-bucket asap_sandbox
```

## Deploy Function

```
sam deploy --template-file packaged-template.yml \
--stack-name dlqExample \
--parameter-overrides snsEmailAddress=email@domain.com \
--capabilities CAPABILITY_IAM
```

eg.

```
sam deploy --template-file packaged-template.yml \
--stack-name dlqExample \
--parameter-overrides snsEmailAddress=email@domain.com \
--capabilities CAPABILITY_IAM
```

# Confirm SNS Topic Subscription

Go to your email application and open the message from AWS Notifications, and then click the link to confirm your subscription. 

# Trigger Execution

The function `longRunningFunction` will be triggered once data is uploaded to the generated input bucket.  A wrapper script can be used to upload a properly formatted file to the generated bucket.  

```
python ../../../sam-projects/utilities/upload_data.py <YOUR STACK NAME> <YOUR FILE NAME>
```

eg.

```
python ../../../sam-projects/utilities/upload_data.py dlqExample index.py
```

# Destroy Stack on AWS

## Clean Up Bucket Contents

In order for Cloudformation to delete the stack the input bucket will first need to be empty.  This can be done by running the following command.

```
python ../../../sam-projects/utilities/bucket_cleaner.py <YOUR STACK NAME>
```

eg.

```
python ../../../sam-projects/utilities/bucket_cleaner.py dlqExample
```

## Delete Cloudformation Stack

Once the generated bucket is empty you can delete the stack using the following command.

```
aws cloudformation delete-stack \
--stack-name <YOUR STACK NAME>
```

eg.

```
aws cloudformation delete-stack \
--stack-name dlqExample
```
