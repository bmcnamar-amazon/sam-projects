# s3ToDynamo

This example will deploy a function that will extract data from a S3 object and insert data into a DynamoDB table.

# Run Function Locally Using sam local

```
sam local invoke s3ToDynamo -e input.json
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
--parameter-overrides ReportBucket=<REPORT BUCKET NAME> \
--capabilities CAPABILITY_IAM
```

eg.

```
aws cloudformation deploy --template-file packaged-template.yml \
--stack-name s3ToDynamo \
--capabilities CAPABILITY_IAM
```

# Additional Notes

Command to return seconds since Epoch (UTC) on a Mac workstation:

```
date -j -f "%a %b %d %T %Z %Y" "`date`" +"%s" -U
```
