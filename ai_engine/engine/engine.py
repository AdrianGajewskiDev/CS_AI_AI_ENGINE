import ast
import json
import os
from typing import List

from ai_engine.dynamo_db.dynamo_db import update_task_status
from ai_engine.helpers.extract_data import extract_data_from_event
from ai_engine.logging.logger import InternalLogger
from ai_engine.model.model import train_model
from ai_engine.seed_data.puller import SeedDataPuller
from ai_engine.seed_data.s3_data_puller import S3DataPuller

RESOLVERS = os.getenv('RESOLVER_NAMES')

def startup_engine(event: dict) -> int:
    task_id, seed_data = extract_data_from_event(event)

    if not seed_data:
        InternalLogger.LogInfo('No seed data found')
        
    price, stats = train_model(seed_data)
    
    update_task_status(task_id=task_id, status='COMPLETED', stats={'processed': stats, 'price': price})

    return 0
