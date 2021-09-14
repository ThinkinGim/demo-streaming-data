from aws_cdk import (
    core,
    aws_ec2,
    aws_s3,
    aws_lambda,
    aws_lambda_event_sources,
    aws_iam,
    aws_msk,
)

class InputStore():

    def __init__(self, scope: core.Construct, id: str, network_vpc: aws_ec2.IVpc, msk_cluster_arn: str, **kwargs) -> None:

        input_store = aws_s3.Bucket(scope, 'streaming_data',
            removal_policy=core.RemovalPolicy.DESTROY
        )

        input_handler_role = aws_iam.Role(scope, "input_handler_role", 
            description="input_handler_role Role",
            assumed_by=aws_iam.ServicePrincipal("lambda.amazonaws.com"),
        )
        input_handler_role.add_managed_policy(
            aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaENIManagementAccess')
        )
        input_handler_role.add_managed_policy(
            aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole')
        )

        input_handler = aws_lambda.Function(scope, 'input_handler',
            function_name='input_handler',
            handler='input_handler.do',
            runtime=aws_lambda.Runtime.PYTHON_3_7,
            code=aws_lambda.Code.asset('artifact/streaming_data/lambda_input_handler'),
            timeout=core.Duration.seconds(300),
            role=input_handler_role,
            vpc=network_vpc,
            environment={
                'input_bucket_name': input_store.bucket_name,
                'msk_cluster_arn': msk_cluster_arn
            }
        )

        input_handler.add_event_source(
            aws_lambda_event_sources.S3EventSource(input_store,events=[aws_s3.EventType.OBJECT_CREATED])
        )

class ProcessingPipeline():

    def __init__(self, scope: core.Construct, id: str, network_vpc: aws_ec2.IVpc, **kwargs) -> None:

        msk = aws_msk.Cluster(scope, 'streaming-pipeline',
            cluster_name='streamingdata',
            kafka_version=aws_msk.KafkaVersion.V2_8_0,
            vpc=network_vpc,
            removal_policy=core.RemovalPolicy.DESTROY
        )

        self.msk_cluster_arn = msk.cluster_arn