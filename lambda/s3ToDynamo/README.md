# s3ToDynamo

This example will deploy a function that will extract data from a S3 object and insert data into a DynamoDB table.

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
--stack-name <YOUR STACK NAME> \
--capabilities CAPABILITY_IAM
```

eg.

```
sam deploy --template-file packaged-template.yml \
--stack-name s3ToDynamo \
--capabilities CAPABILITY_IAM
```

# Trigger Execution

The function `s3ToDynamo` will be triggered once data is uploaded to the generated bucket.  A wrapper script can be used to upload a properly formatted file to the generated bucket.  

```
python upload_data.py <YOUR STACK NAME> <YOUR FILE NAME>
```

eg.

```
python upload_data.py s3ToDynamo sample.json
```

Once the data is uploaded to S3 there should be corresponding entries in the `stock-prices-s3ToDynamo` DynamoDB table.

# Destroy Stack on AWS

## Clean Up Bucket Contents

In order for Cloudformation to delete the stack the input bucket will first need to be empty.  This can be done by running the following command.

```
python bucket_cleaner.py <YOUR STACK NAME>
```

eg.

```
python bucket_cleaner.py s3ToDynamo
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
--stack-name s3ToDynamo
```

# Additional Notes

Command to return seconds since Epoch (UTC) on a Mac workstation:

```
date -j -f "%a %b %d %T %Z %Y" "`date`" +"%s" -U
```
