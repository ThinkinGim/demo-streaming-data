from aws_cdk import core
from artifact import (
    event_store,
    infra,
)

class StreamingDataScenarioStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        network = infra.Network(self, 'infra')
        s3_bucket = event_store.S3(self, 'event_store')
