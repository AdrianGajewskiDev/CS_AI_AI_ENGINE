import os
import boto3

TASKS_TABLE_NAME = os.getenv("TASK_TABLE_NAME", "")

def update_task_status(task_id: str, status: str, stats: dict = {}):
    dynamodb = boto3.client('dynamodb')
    dynamodb.update_item(
        TableName=TASKS_TABLE_NAME,
        Key={
            'task_id': {
                'S': task_id
            }
        },
        UpdateExpression="set #status = :status, #processed = :processed, #recommended_price = :price",
        ExpressionAttributeNames={
            "#status": "status",
            "#processed": "processed",
            "#recommended_price": "recommended_price"
        },
        ExpressionAttributeValues={
            ":status": {
                'S': status
            },
            ":processed": {
                'N': str(stats.get('processed', 0))
            },
            ":price": {
                'N': str(stats.get('price', 0))
            }
        }
    )