from ai_engine.engine.engine import startup_engine


def handler(event: dict, context):
    return startup_engine(event)