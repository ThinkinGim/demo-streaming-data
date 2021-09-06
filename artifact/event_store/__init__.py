from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_s3,
)

class S3():

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:

        s3 = aws_s3.Bucket(scope, 'event_store')
