# sam-projects

The purpose of this project is to hack on things to deploy via SAM.

## Prerequisites

### AWS CLI
The project depends upon having the [AWS CLI](https://aws.amazon.com/cli/) being installed and available.

#### Mac and Linux

The AWS CLI can be installed using the Python pip package utility.  It is possible to create isolated Python environments using [Virtualenv](https://virtualenv.pypa.io/en/stable/).  Though not required, it makes standardizing packages on a project much easier.

```
pip install -r requirements.txt
```

Once the CLI is installed it must be configured with IAM keys:

```
aws configure
```

#### Windows

Download and run the [64-bit](https://s3.amazonaws.com/aws-cli/AWSCLI64.msi) or [32-bit](https://s3.amazonaws.com/aws-cli/AWSCLI32.msi) Windows installer.

Once the CLI is installed it must be configured with IAM keys:

```
aws configure
```

### Node.js

SAM Local depends upon Node.js and NPM (Node Package Manager) being installed.  Please download and install the version of Node.js from the [Downloads](https://nodejs.org/en/download/) site that is suitable to your operating system.

### SAM and SAM Local

The project allows artifacts to be deployed using the [Serverless Application Model (SAM)](https://github.com/awslabs/serverless-application-model) and [SAM Local](https://github.com/awslabs/aws-sam-local).

For instructions on installing specific prerequisites, please refer to the [Prerequisites](https://github.com/awslabs/aws-sam-local#prerequisites) section of the SAM Local Github project.

### AWS S3 Bucket

The projects included in this repository will upload code to a S3 bucket.  This bucket will be referenced in directions using the convention `<YOUR S3 BUCKET>`.  Once the AWS CLI is configured, create your bucket.  Bucket names must be unique so copying and pasting the example using asap_sandbox will fail as the bucket already exists.

```
aws s3 mb s3://<YOUR S3 BUCKET>
```

eg.

```
aws s3 mb s3://asap_sandbox
```
