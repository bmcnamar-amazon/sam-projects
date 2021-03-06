# versionsAndAliases

This example will highlight how function versioning and aliasing can be used.  In order to see the effect of the deploy, run multiple package and deploy cycles.  The function script will return the output the executed version and the ARN.  The ARN will include the alias name.

The important takeaway is that the directive `AutoPublishAlias` will automatically increment the deployed version and associate the alias to the new version.

This example also creates an [output and export](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/outputs-section-structure.html) so the function ARN can be referenced from other CloudFormation stacks.

# Run Function Locally Using sam local

```
sam local invoke aliasFunction -e input.json
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

## Deploy Function

```
sam deploy --template-file packaged-template.yml \
--stack-name <YOUR STACK NAME>-<ENVIRONMENT> \
--capabilities CAPABILITY_IAM
```

eg.

```
sam deploy --template-file packaged-template.yml \
--stack-name versionsAndAliases-DEV \
--parameter-overrides Environment=DEV \
--capabilities CAPABILITY_IAM
```

or 

```
sam deploy --template-file packaged-template.yml \
--stack-name versionsAndAliases-PROD \
--parameter-overrides Environment=PROD \
--capabilities CAPABILITY_IAM
```

# Trigger Execution

```
aws lambda invoke \
--invocation-type RequestResponse \
--function-name aliasFunction-DEV \
--qualifier DEV \
outfile.txt
```

or

```
aws lambda invoke \
--invocation-type RequestResponse \
--function-name aliasFunction-PROD \
--qualifier PROD \
outfile.txt
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
--stack-name versionsAndAliases-DEV
```

or

```
aws cloudformation delete-stack \
--stack-name versionsAndAliases-PROD
```
