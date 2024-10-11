import sys
from ai_engine.engine.engine import startup_engine


def handler(event: dict, context):
    return startup_engine(event)

def batch_handler(task_id: str): 
    return startup_engine(task_id)

if __name__ == '__main__':
    args = sys.argv

    if len(args) == 2:
        task_id = args[1]
        batch_handler("172cd7b5-0e6e-4c66-bdcd-f7b9967c9201")
    
    raise Exception('Invalid arguments')