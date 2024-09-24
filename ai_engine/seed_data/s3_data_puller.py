import os
from typing import List
from ai_engine.seed_data.puller import SeedDataPuller
import boto3
import json


class S3DataPuller(SeedDataPuller):
    _bucket_name: str

    def __init__(self):
        self._bucket_name = os.getenv('RESULTS_BUCKET')

    def pull(self, **kwargs) -> dict:
        try:
            self._key = kwargs.get('key')
            s3 = boto3.client('s3')

            response = s3.get_object(Bucket=self._bucket_name, Key=self._key)
            content = response['Body'].read().decode('utf-8')
            data = json.loads(content)
            return data
        except:
            return {}