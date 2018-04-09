# xrayFunction

This example will deploy a function that is instrumented to use [AWS X-Ray](https://aws.amazon.com/xray).

You will need to copy the file xray-input.sample.json to xray-input.json and include a valid S3 bucket and key and invalid bucket and key as your input object to the Lambda function.  If you do not do this the function will not work.

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
--stack-name xrayFunction \
--capabilities CAPABILITY_IAM
```

# Trigger Execution

```
aws lambda invoke \
--function-name xrayFunction  \
--payload file://xray-input.json \
--region us-east-1 \
output.txt
```

# Destroy Stack on AWS

```
aws cloudformation delete-stack \
--stack-name <YOUR STACK NAME>
```

eg.

```
aws cloudformation delete-stack \
--stack-name xrayFunction
```
