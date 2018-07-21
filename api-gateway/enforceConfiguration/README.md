# enforceConfiguration

At present, API Gateway does not integrate with either Config or CloudWatch Events.  This makes it difficult to determine whether a REST endpoint falls out of compliance.

The purpose of this Lambda function is to iterate through all API Gateway REST endpoints (default: 1min interval) and determine whether:

* The authtype is custom

* The authorizer type is token

* The authorizerUrl is a user-supplied Lambda function

Failure on any of these parameters will result in the Lambda function erroring.

At this point, the example is crude.  There are several shortcomings:

* The Lambda function that checks configuration is triggered by rate, not changes to any API.  This can be addressed by triggering functions based upon CloudWatch API calls

* All stages of all API Gateway are checked.  This may be too broad a definition.  This can be addressed by passing in API Gateway value(s) and stage name(s) as environment variables to the configuration checking function.

# Deploy Function to AWS

## Package the Function Using SAM CLI

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

## Deploy Function Using SAM CLI

```
sam deploy --template-file packaged-template.yml \
--stack-name enforceConfiguration \
--parameter-overrides LambdaAuthorizerArn=<ARN OF LAMBDA AUTHORIZER> RateExpression=<VALID RATE EXPRESSION> \
--capabilities CAPABILITY_IAM
```

eg.

```
sam deploy --template-file packaged-template.yml \
--stack-name enforceConfiguration \
--parameter-overrides LambdaAuthorizerArn=arn:aws:lambda:aws_region:your_account_id:function:your_function RateExpression="rate(1 minute)" \
--capabilities CAPABILITY_IAM
```

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
--stack-name enforceConfiguration
```
