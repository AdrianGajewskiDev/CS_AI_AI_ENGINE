import ast
import json
import os
from typing import List
from cs_ai_common.logging.internal_logger import InternalLogger
from ai_engine.seed_data.puller import SeedDataPuller
from ai_engine.seed_data.s3_data_puller import S3DataPuller

RESOLVERS = os.getenv('RESOLVER_NAMES')

def extract_data_from_event(event: dict | str):
    records = event.get('Records') if isinstance(event, dict) else event
    if not records and isinstance(event, dict):
        InternalLogger.LogError('No records found in the event')
        return None, None
    
    # sns always sends a single record
    return _process_record(records[0] if isinstance(records, list) else event)


def _process_record(record: dict | str) -> None:
    if isinstance(record, dict):
        sns = record.get('Sns', {})
        message = sns.get('Message')
        task_id = _extract_task_id(message)
    else:
        task_id = record

    if not task_id:
        InternalLogger.LogError('No task_id found in the message')
        raise

    InternalLogger.LogDebug(f'Processing task_id: {task_id}')
    data = _pull_data(task_id, S3DataPuller())
    InternalLogger.LogDebug(f'Pulled data: {data}')
    return task_id, data

def _pull_data(task_id: str, data_puller: SeedDataPuller) -> List[dict]:
    _resolver = ast.literal_eval(RESOLVERS)

    InternalLogger.LogDebug(f'Found resolvers: {_resolver}')

    if not _resolver:
        InternalLogger.LogError('No resolvers found')
        raise
    
    resolved_data: list = []
    for resolver in _resolver:
        _resolver_name_short = _get_resolver_name_short(resolver)
        key = _build_key(task_id, _resolver_name_short)
        InternalLogger.LogDebug(f'Pulling data for task_id: {task_id} and resolver: {_resolver_name_short}')
        data = data_puller.pull(key=key)
        if not data:
            InternalLogger.LogError(f'No data found for task_id: {task_id} and resolver: {_resolver_name_short}')
            continue
        
        content = data.get('content')
        if not content:
            InternalLogger.LogError(f'No content found for task_id: {task_id} and resolver: {_resolver_name_short}')
            continue
        InternalLogger.LogDebug(f'Found content for task_id: {task_id} and resolver: {_resolver_name_short}')
        InternalLogger.LogDebug(f'Content: {content}')
        resolved_data += [json.loads(_content) for _content in content]

    return resolved_data 

def _get_resolver_name_short(resolver: str) -> str:
    return resolver.split('-')[2]

def _build_key(task_id: str, resolver: str) -> str:
    return f'{task_id}/{resolver}/result.json'

def _extract_task_id(message) -> str:
    if not message:
        InternalLogger.LogError('No message found in the record')
        raise
    InternalLogger.LogDebug(f'Extracting task_id from message: {message}')
    try:
        message = json.loads(message)
    except json.JSONDecodeError as e:
        InternalLogger.LogError(f'Failed to parse message: {str(e)}')
        raise

    return message.get('task_id')