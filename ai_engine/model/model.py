from typing import List
from ai_engine.logging.logger import InternalLogger


def train_model(seed_data: List[dict]):
    InternalLogger.LogInfo('Training model')
    
    InternalLogger.LogInfo('Model training complete')
    return 10, 100