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
