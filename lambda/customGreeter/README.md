# customGreeter

This example will deploy a very simple Lambda function written in Python that will allow for customized input fields.

# Run Function Locally Using sam local

```
sam local invoke customGreeter -e event.json
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

## Deploy Function Using Cloudformation

```
aws cloudformation deploy --template-file packaged-template.yml \
--stack-name <YOUR STACK NAME> \
--capabilities CAPABILITY_IAM
```

eg.

```
aws cloudformation deploy --template-file packaged-template.yml \
--stack-name customGreeter \
--capabilities CAPABILITY_IAM
```
