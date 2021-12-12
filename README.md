# Pulumi-tutorial
how to use pulumi step by step

## lv.0
```zsh
pulumi new aws-python
```
```zsh
pulumi up
```

## lv.1
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