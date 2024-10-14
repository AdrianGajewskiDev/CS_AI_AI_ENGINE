import sys
from ai_engine.engine.engine import startup_engine
from cs_ai_common.startup.startup import startup_app


def handler(event: dict, context):
    return startup_engine(event)

def batch_handler(task_id: str): 
    return startup_engine(task_id)

if __name__ == '__main__':
    args = sys.argv

    if len(args) == 2:
        task_id = args[1]
        print("Task ID: ", task_id)
        startup_app(
            lambda: batch_handler(task_id),
            retry_on=None,
            retries=1,
            raw_event={"task_id": task_id}
        )
    else:
        raise Exception('Invalid arguments')