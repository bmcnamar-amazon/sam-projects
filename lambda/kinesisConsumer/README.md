# kinesisConsumer

This application will deploy several resources.  The intent is to demonstrate how Lambda consumers can take data from a Kinesis stream to publish to a DynamoDB table and S3 for later use.

# Deploy Stack to AWS

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

## Deploy Stack

```
sam deploy --template-file packaged-template.yml \
--stack-name <YOUR STACK NAME> \
--capabilities CAPABILITY_IAM
```

eg.

```
sam deploy --template-file packaged-template.yml \
--stack-name kinesisConsumer \
--capabilities CAPABILITY_IAM
```

# Trigger Execution - Insert

The functions `handler` in `code/dynamo.py` and `code/s3.py` will be triggered once data is uploaded to the Kinesis stream.  A wrapper script can upload properly formatted data to the generated bucket.

Use the following command to identify the Kinesis stream name generated by the SAM template. 

```
python ../../../sam-projects/utilities/kinesis_stream.py <YOUR STACK NAME>
```

eg.

```
python ../../../sam-projects/utilities/kinesis_stream.py kinesisConsumer
```

Once the stream name is identified, sample data can be published using the `generate_data.py` script.

```
python generate_data.py <KINESIS STREAM NAME>
```

eg.

```
python generate_data.py kinesisConsumer-InputStream-ABC123
```


# Destroy Stack on AWS

## Clean Up Bucket Contents

In order for Cloudformation to delete the stack the input bucket will first need to be empty.  This can be done by running the following command.

```
python ../../../sam-projects/utilities/bucket_cleaner.py <YOUR STACK NAME>
```

eg.

```
python ../../../sam-projects/utilities/bucket_cleaner.py kinesisConsumer
```

## Delete Cloudformation Stack

Once the generated buckets are empty you can delete the stack using the following command.

```
aws cloudformation delete-stack \
--stack-name <YOUR STACK NAME>
```

eg.

```
aws cloudformation delete-stack \
--stack-name kinesisConsumer
```