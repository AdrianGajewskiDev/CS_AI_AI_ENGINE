import ast
import json
import os
from typing import List

from ai_engine.dynamo_db.dynamo_db import get_task_seed_data, update_task_status
from ai_engine.helpers.extract_data import extract_data_from_event
from ai_engine.model.model import predict_price
from ai_engine.related.get_most_related import get_most_related
from ai_engine.s3.s3 import upload_recommendation_results
from ai_engine.sns.sns import publish_to_sns
from ai_engine.utils.combine_results import combine_results
from cs_ai_common.logging.internal_logger import InternalLogger

RESOLVERS = os.getenv('RESOLVER_NAMES')

def startup_engine(event: dict | str) -> int:
    InternalLogger.LogDebug('Starting engine')

    task_id, resolved_data = extract_data_from_event(event)

    if not resolved_data:
        InternalLogger.LogDebug('No seed data found')
        update_task_status(task_id=task_id, status='NOT_ENOUGH_DATA')
        return -1
    
    update_task_status(task_id=task_id, status='ANALYZING')

    InternalLogger.LogDebug('Getting seed data')

    seed_data = get_task_seed_data(task_id)
    
    InternalLogger.LogDebug('Training model')
    
    price = predict_price(resolved_data, seed_data)
    
    InternalLogger.LogDebug('Getting most related')
    
    most_related = get_most_related(resolved_data, seed_data)
    
    InternalLogger.LogDebug('Combining results')
    
    result = combine_results(price, most_related)
    
    InternalLogger.LogDebug('Uploading results')
    
    upload_recommendation_results(json.dumps(result), task_id)

    InternalLogger.LogDebug('Updating task status')

    update_task_status(task_id=task_id, status='COMPLETED')

    publish_to_sns(task_id)
    return 0
