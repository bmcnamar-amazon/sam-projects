# enforceConfiguration

At present, API Gateway does not integrate with either Config or CloudWatch Events.  This makes it difficult to determine whether a REST endpoint falls out of compliance.

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
