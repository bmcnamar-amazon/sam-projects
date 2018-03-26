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
--stack-name whatIsMyIpPartDeux \
--capabilities CAPABILITY_IAM
```

# Deploy to an Alternate Region (not us-east-1)

```
sam package --template-file template.yml \
--output-template-file packaged-template.yml \
--s3-bucket <YOUR S3 BUCKET NOT IN US-EAST-1>
```

eg.

```
sam package --template-file template.yml \
--output-template-file packaged-template.yml \
--s3-bucket asap-sandbox-us-east-2
```

## Deploy Function Using Cloudformation

```
sam deploy --template-file packaged-template.yml \
--stack-name <YOUR STACK NAME> \
--region us-east-2 \
--capabilities CAPABILITY_IAM
```

eg.

```
sam deploy --template-file packaged-template.yml \
--stack-name whatIsMyIp \
--region us-east-2 \
--capabilities CAPABILITY_IAM
```
