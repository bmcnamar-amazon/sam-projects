# helloWorldPython

This example will deploy a very simple 'Hello World' Lambda function written in Python.

# Run Function Locally Using sam local

```
sam local invoke PythonHelloWorldFunction -e event.json
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
--stack-name helloWorldPython \
--capabilities CAPABILITY_IAM
```
