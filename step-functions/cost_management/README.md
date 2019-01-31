# cost_management

[Cost Optimization](https://d1.awsstatic.com/whitepapers/architecture/AWS-Cost-Optimization-Pillar.pdf) is one of the pillars of AWS' [Well Architected Framework](https://aws.amazon.com/architecture/well-architected/).

The intent of this example is to show how numerous cost savings functions can be chained together through the use of Step Functions.

# Deploy Application to AWS

## Package the Application

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

## Deploy Application

```
sam deploy --template-file packaged-template.yml \
--stack-name <YOUR STACK NAME> \
--capabilities CAPABILITY_IAM
```

eg.

```
sam deploy --template-file packaged-template.yml \
--stack-name costManagement \
--capabilities CAPABILITY_IAM
```

# Destroy Stack on AWS

## Delete Cloudformation Stack


```
aws cloudformation delete-stack \
--stack-name <YOUR STACK NAME>
```

eg.

```
aws cloudformation delete-stack \
--stack-name costManagement
```

