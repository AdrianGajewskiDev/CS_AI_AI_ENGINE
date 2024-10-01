import json
import os
import boto3

TASKS_TABLE_NAME = os.getenv("TASK_TABLE_NAME", "")

def update_task_status(task_id: str, status: str):
    dynamodb = boto3.client('dynamodb')
    dynamodb.update_item(
        TableName=TASKS_TABLE_NAME,
        Key={
            'task_id': {
                'S': task_id
            }
        },
        UpdateExpression="set #status = :status",
        ExpressionAttributeNames={
            "#status": "status",
        },
        ExpressionAttributeValues={
            ":status": {
                'S': status
            }
        }
    )

def get_task_seed_data(task_id: str) -> dict:
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.get_item(
        TableName=TASKS_TABLE_NAME,
        Key={
            'task_id': {
                'S': task_id
            }
        }
    )
    return json.loads(response.get('Item', {}).get('seed_data', {}).get('S', {}))