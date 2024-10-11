import sys
from ai_engine.engine.engine import startup_engine


def handler(event: dict, context):
    return startup_engine(event)

def batch_handler(task_id: str): 
    return startup_engine({'Records': [{'Sns': {'Message': task_id}}]})

if __name__ == '__main__':
    args = sys.argv

    if len(args) == 2:
        task_id = args[2]
        batch_handler(task_id)
    
    raise Exception('Invalid arguments')