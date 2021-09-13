from aws_cdk import core
from artifact import (
    streaming_data,
    infra,
)

class StreamingDataScenarioStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        network = infra.Network(self, 'infra')
        s3_bucket = streaming_data.InputStore(self, 'input_store', network_vpc=network.vpc)
