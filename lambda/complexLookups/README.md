# complexLookups

The actual function itself is very simple.  It will only print out an environment variable associated with the function.  What is being highlighted is the ability to do complex lookups based upon input parameters.

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
--stack-name complexLookups \
--parameter-overrides StackPrefix=test StackEnvironment=dev \
--capabilities CAPABILITY_IAM
```

# Trigger Execution

The following invocation assumes the exact steps above were used to deploy the function.

```
aws lambda invoke --invocation-type RequestResponse --function-name test-lambdas-Preprocess-dev outfile.txt
```

# Destroy Stack on AWS

## Delete Cloudformation Stack

Once the generated bucket is empty you can delete the stack using the following command.

```
aws cloudformation delete-stack \
--stack-name <YOUR STACK NAME>
```

eg.

```
aws cloudformation delete-stack \
--stack-name complexLookup
```
