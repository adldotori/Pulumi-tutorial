# Pulumi-tutorial
how to use pulumi step by step

### [lv.0 : Get Started](#lv0--get-started)  
### [lv.1 : Deploy Static HTML](#lv1--deploy-static-html)  
### [lv.2 : Running Containers on EC2 Fargate](#lv2--running-containers-on-ecs-fargate)  
### [lv.3 : Deploy a Webserver to AWS EC2](#lv3--deploy-a-webserver-to-aws-ec2)  
### [With Copilot](#with-copilot)  

## lv.0 : Get Started
https://www.pulumi.com/docs/get-started/
```zsh
$ brew install pulumi # install pulumi
$ export AWS_ACCESS_KEY_ID=<YOUR_ACCESS_KEY_ID>
$ export AWS_SECRET_ACCESS_KEY=<YOUR_SECRET_ACCESS_KEY>
$ mkdir lv.0 && cd lv.0 # make new folder
$ pulumi new aws-python # creating a new Pulumi project
```

### \_\_main\_\_.py
```python
import pulumi
from pulumi_aws import s3

# Create an AWS resource (S3 Bucket)
bucket = s3.Bucket('my-bucket')

# Export the name of the bucket
pulumi.export('bucket_name',  bucket.id)
```
```
$ pulumi up ; deploy your stack
```
Now that your bucket has been provisioned
```zsh
$ pulumi stack
```
```zsh
Current stack is dev:
    Owner: adldotori
    Last updated: 8 seconds ago (2021-12-13 13:02:36.022555 +0900 KST)
    Pulumi version: v3.19.0
Current stack resources (3):
    TYPE                     NAME
    pulumi:pulumi:Stack      lv.0-dev
    ├─ aws:s3/bucket:Bucket  my-bucket
    └─ pulumi:providers:aws  default_4_32_0

Current stack outputs (1):
    OUTPUT       VALUE
    bucket_name  my-bucket-b286cda

```

## lv.1 : Deploy Static HTML
https://www.pulumi.com/docs/get-started/aws/modify-program/
### \_\_main\_\_.py
```python
"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import s3

# Create an AWS resource (S3 Bucket)
bucket = s3.Bucket('my-bucket',
    website=s3.BucketWebsiteArgs(
        index_document="index.html",
    ))

# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)

bucketObject = s3.BucketObject(
    'index.html',
    acl='public-read',
    content_type='text/html',
    bucket=bucket,
    source=pulumi.FileAsset('index.html'),
)

pulumi.export('bucket_endpoint', pulumi.Output.concat('http://', bucket.website_endpoint))
```
You can check out your new static website.

test url : [http://my-bucket-278ca8d.s3-website-us-east-1.amazonaws.com](http://my-bucket-278ca8d.s3-website-us-east-1.amazonaws.com)


## lv.2 : Running Containers on ECS "Fargate"
https://www.pulumi.com/registry/packages/aws/how-to-guides/ecs-fargate/

Build and publish a Docker Container to a private Elastic Container Registry and spin up a load-balanced Amazon Elastic Container Service Fargate service.

```zsh
$ pulumi stack

    Type                                          Name                        Status       Info
     pulumi:pulumi:Stack                           lv.2-dev                    running..    read aws:ec2:Subnet default-vpc-public-0
     ├─ awsx:x:ecs:FargateTaskDefinition           nginx                                    0664b7821b60: Pushed
     pulumi:pulumi:Stack                           lv.2-dev                    running      read aws:ec2:Subnet default-vpc-public-0
     pulumi:pulumi:Stack                           lv.2-dev                    running.     read aws:ec2:Subnet default-vpc-public-0
 ~   │  ├─ aws:cloudwatch:LogGroup                 nginx                       updated      
 +   │  ├─ aws:iam:RolePolicyAttachment            nginx-task-0cbb1731         created      
 +   │  ├─ aws:iam:RolePolicyAttachment            nginx-task-b5aeb6b6         created      
 +   │  ├─ aws:iam:RolePolicyAttachment            nginx-execution-58ed699a    created      
 +   │  ├─ aws:iam:RolePolicyAttachment            nginx-execution-9a42f520    created      
     ├─ awsx:x:ecs:FargateTaskDefinition           nginx                                   1 warning
     ├─ awsx:x:ec2:Vpc                             default-vpc                             
 +   │  ├─ awsx:x:ec2:Subnet                       default-vpc-public-0        created     
 +   │  └─ awsx:x:ec2:Subnet                       default-vpc-public-1        created     
     ├─ awsx:lb:NetworkLoadBalancer                nginx                                   
     │  ├─ awsx:lb:NetworkTargetGroup              nginx                                   
 +   │  │  └─ aws:lb:TargetGroup                   nginx                       created     
 +   │  ├─ aws:lb:LoadBalancer                     nginx                       created     
     │  └─ awsx:lb:NetworkListener                 nginx                                   
 +   │     └─ aws:lb:Listener                      nginx                       created     
     ├─ awsx:x:ecs:Cluster                         default-cluster                         
     │  └─ awsx:x:ec2:SecurityGroup                default-cluster                         
 +   │     ├─ aws:ec2:SecurityGroup                default-cluster             created     
     │     ├─ awsx:x:ec2:IngressSecurityGroupRule  default-cluster-containers              
 +   │     │  └─ aws:ec2:SecurityGroupRule         default-cluster-containers  created     
     │     ├─ awsx:x:ec2:EgressSecurityGroupRule   default-cluster-egress                  
 +   │     │  └─ aws:ec2:SecurityGroupRule         default-cluster-egress      created     
     │     └─ awsx:x:ec2:IngressSecurityGroupRule  default-cluster-ssh                     
 +   │        └─ aws:ec2:SecurityGroupRule         default-cluster-ssh         created     
     └─ awsx:x:ecs:FargateService                  nginx                                   
 +      └─ aws:ecs:Service                         nginx                       created  
 ```

test url : [http://nginx-c06dc0c-8e5a583c32cabe91.elb.ap-northeast-2.amazonaws.com/](http://nginx-c06dc0c-8e5a583c32cabe91.elb.ap-northeast-2.amazonaws.com/)

## lv.3 : Deploy a Webserver to AWS EC2
https://www.pulumi.com/registry/packages/aws/how-to-guides/ec2-webserver/
```python
server = aws.ec2.Instance('webserver-www',
    instance_type=size,
    vpc_security_group_ids=[group.id], # reference security group from above
    user_data=user_data, # <-- ADD THIS LINE
    ami=ami.id)
```

```zsh
$ pulumi stack

Current stack is dev:
    Owner: adldotori
    Last updated: 12 minutes ago (2021-12-12 23:14:36.700443 +0900 KST)
    Pulumi version: v3.19.0
Current stack resources (5):
    TYPE                                    NAME
    pulumi:pulumi:Stack                     lv.3-dev
    ├─ aws:ec2/securityGroup:SecurityGroup  webserver-secgrp
    ├─ aws:ec2/instance:Instance            webserver-www
    ├─ pulumi:providers:aws                 default
    └─ pulumi:providers:aws                 default_4_32_0

Current stack outputs (2):
    OUTPUT          VALUE
    publicHostName  ec2-3-34-191-142.ap-northeast-2.compute.amazonaws.com
    publicIp        3.34.191.142

More information at: https://app.pulumi.com/adldotori/lv.3/dev
```

test url : [http://3.34.191.142/](http://3.34.191.142/)

## With Copilot
Only the three lines below are the codes I wrote.

```python
# Create an AWS resource (S3 Bucket) and deploy static files (index.html) to the bucket.
import pulumi
import pulumi_aws as aws
```

Then ....
```python
# Only the three lines below are the codes I wrote.

# --------------------------------------------------
# Create an AWS resource (S3 Bucket) and deploy static files (index.html) to the bucket.
import pulumi
import pulumi_aws as aws
# --------------------------------------------------

# Create an S3 Bucket
bucket = aws.s3.Bucket("bucket")


# Create an index.html file in our project
index_html = """<html>
    <body>
        <h1>Hello, World!</h1>
    </body>
</html>
"""


# Create a file resource in Pulumi
index_html_file = pulumi.FileAsset(index_html)


# Create a file in S3
aws.s3.BucketObject("index",
    bucket=bucket.id,
    key="index.html",
    source=index_html_file)


# Export the bucket name
pulumi.export("bucket", bucket.bucket)
pulumi.export("bucket_url", bucket.website_endpoint)
```

Copilot recommends Infrastructure for our goals!  
It's really amazing.
