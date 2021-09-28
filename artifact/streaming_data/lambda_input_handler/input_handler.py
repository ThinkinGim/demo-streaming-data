import os
import boto3

MSK_CLUSTER = os.environ['msk_cluster_arn']

CLIENT = boto3.client('kafka')
RESPONSE = CLIENT.get_bootstrap_brokers(
    ClusterArn=MSK_CLUSTER
)

def do(event: dict, context):
    print(RESPONSE)