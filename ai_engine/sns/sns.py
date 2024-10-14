import json
import os
import boto3

from cs_ai_common.logging.internal_logger import InternalLogger

SNS_TOPIC_ARN = os.getenv('SNS_TOPIC_ARN')

def publish_to_sns(task_id: str) -> None:
    InternalLogger.LogDebug('Publishing to SNS')
    
    sns = boto3.client('sns')
    
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=json.dumps({
            "default": json.dumps({"task_id": task_id}),
        }),
        MessageStructure='json'
    )