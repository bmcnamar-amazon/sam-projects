# mongodb

This application will deploy several resources.  The intent is to demonstrate how Lambda consumers can take data from a Kinesis stream to publish to a MongoDB database and query the MongoDB database.

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
--parameter-overrides SsmConfigName=<YOUR CONFIG SPACE IN SSM> MongoDatabaseName=<YOUR DATABASE NAME> \
--capabilities CAPABILITY_IAM
```

eg.

```
sam deploy --template-file packaged-template.yml \
--stack-name mongoExample \
--parameter-overrides SsmConfigName=mdbw2018 MongoDatabaseName=games \
--capabilities CAPABILITY_IAM
```

# Trigger Execution - Insert

The function `InsertToMongo` will be triggered once data is uploaded to the Kinesis stream.  A wrapper script can be used to upload a properly formatted file to the generated bucket.  

```
python ../../../sam-projects/utilities/kinesis_stream.py <YOUR STACK NAME>
```

eg.

```
python ../../../sam-projects/utilities/kinesis_stream.py mongoExample
```

Once the stream name is identified, sample data can be published using the `generate_data.py` script.

```
python generate_data.py <KINESIS STREAM NAME>
```

eg.

```
python generate_data.py mongoExample-InputStream-ABC123
```

# Trigger Execution - Query

Work in progress.


# Destroy Stack on AWS

## Delete Cloudformation Stack

Once the generated buckets are empty you can delete the stack using the following command.

```
aws cloudformation delete-stack \
--stack-name <YOUR STACK NAME>
```

eg.

```
aws cloudformation delete-stack \
--stack-name mongoExample
```
