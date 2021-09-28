import os
import boto3
from kafka import KafkaProducer
from json import dumps

MSK_CLUSTER = os.environ['msk_cluster_arn']

CLIENT = boto3.client('kafka')
RESPONSE = CLIENT.get_bootstrap_brokers(
    ClusterArn=MSK_CLUSTER
)

PRODUCER = KafkaProducer(
    acks=0, 
    compression_type='gzip', 
    bootstrap_servers=['localhost:9092'], 
    value_serializer=lambda x: dumps(x).encode('utf-8'))

def do(event: dict, context):
    print(RESPONSE)

    data = {'str' : 'result-test'}
    PRODUCER.send('test', value=data)
    PRODUCER.flush()
    