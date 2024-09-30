import os
import boto3

RECOMMENDATIONS_BUCKET = os.getenv("RECOMMENDATIONS_BUCKET")

def upload_recommendation_results(results: str, task_id: str) -> None:
    s3_client = boto3.client('s3')
    file_name = f'recommendations/{task_id}.json'

    s3_client.put_object(
        Bucket=RECOMMENDATIONS_BUCKET,
        Key=file_name,
        Body=results
    )