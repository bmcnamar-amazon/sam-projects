# jsonToPdf

This example will deploy a function that will create a PDF based upon a JSON document.

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

## Deploy Function Using Cloudformation

```
aws cloudformation deploy --template-file packaged-template.yml \
--stack-name <YOUR STACK NAME> \
--capabilities CAPABILITY_IAM
```

eg.

```
sam deploy --template-file packaged-template.yml \
--stack-name jsonToPdf \
--capabilities CAPABILITY_IAM
```

# Trigger Execution

The function `jsonToPDF` will be triggered once data is uploaded to the input bucket.  A wrapper script can be used to upload a properly formatted file to the generated bucket.  

```
python upload_data.py <YOUR STACK NAME> <YOUR FILE NAME>
```

eg.

```
upload_data.py jsonToPdf input.json
```

Once the data is uploaded to S3 there should be corresponding PDF reports entries in the output bucket.

# Destroy Stack on AWS

## Clean Up Bucket Contents

In order for Cloudformation to delete the stack the input bucket will first need to be empty.  This can be done by running the following command.

```
python bucket_cleaner.py <YOUR STACK NAME>
```

eg.

```
python bucket_cleaner.py jsonToPdf
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
--stack-name jsonToPdf
```
