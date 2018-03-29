# whatismyip

This example will create and deploy a Lambda function and API Gateway endpoint that simply returns the requester's IP address.

# Run Function Locally Using sam local

```
sam local invoke whatIsMyIp -e input.json
```

# Deploy Function to AWS

## Package the Function to us-east-1

The S3 bucket referenced in my example resides in us-east-1.  The default behavior is to deploy to us-east-1.

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
sam deploy --template-file packaged-template.yml \
--stack-name <YOUR STACK NAME> \
--capabilities CAPABILITY_IAM
```

eg.

```
sam deploy --template-file packaged-template.yml \
--stack-name whatIsMyIp \
--capabilities CAPABILITY_IAM
```

# Visit the API Endpoint

Run the following command to return the URL of the generated resource.

```
python get_url.py <YOUR STACK NAME>
```

eg.

```
python get_url.py whatIsMyIp
```

Once you have the URL you can use command line tools like curl or GUIs like Postman to retrieve results.

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
--stack-name whatIsMyIp
```
