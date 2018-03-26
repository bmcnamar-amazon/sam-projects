# jsonToPdf

This example will deploy a function that will create a PDF based upon a JSON document.

# Run Function Locally Using sam local

```
sam local invoke jsonToPDF -e input.json
```

# Create a S3 Bucket to Store Code

Bucket names in AWS S3 must be globally unique.

```
aws s3 mb s3://<S3 BUCKET NAME>
```

eg.

```
aws s3 mb s3://asap_sandbox
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
--stack-name jsonToPdf \
--parameter-overrides ReportBucket=asap-pdf-output \
--capabilities CAPABILITY_IAM
```

# Invoke Function Using the AWS CLI

```
aws lambda invoke \
--invocation-type RequestResponse \
--function-name jsonToPDF \
--payload file:///${PWD}/input.json \
outfile.txt
```
