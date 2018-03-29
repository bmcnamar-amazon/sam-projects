# jsonToPdf

This example will deploy a function that will create a PDF based upon a JSON document.

# Run Function Locally Using sam local

```
sam local invoke jsonToPDF -e input.json
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
sam deploy --template-file packaged-template.yml \
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
