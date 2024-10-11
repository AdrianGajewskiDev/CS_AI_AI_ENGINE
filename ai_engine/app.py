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
        batch_handler("11e4ab08-a191-478a-87bb-d67424409977")
    else:
        raise Exception('Invalid arguments')