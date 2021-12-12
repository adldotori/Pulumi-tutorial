# Pulumi-tutorial
how to use pulumi step by step

## lv.0 : Get Started
```zsh
pulumi new aws-python
```
```zsh
pulumi up
```

## lv.1 : Deploy Static HTML
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
test url : [http://my-bucket-278ca8d.s3-website-us-east-1.amazonaws.com](http://my-bucket-278ca8d.s3-website-us-east-1.amazonaws.com)


## lv.2 : Containers on ECS "Fargate"
Build and publish a Docker Container to a private Elastic Container Registry and spin up a load-balanced Amazon Elastic Container Service Fargate service.

```zsh
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