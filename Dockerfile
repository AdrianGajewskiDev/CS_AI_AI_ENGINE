FROM public.ecr.aws/lambda/python:3.12

COPY . ${LAMBDA_TASK_ROOT}

RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev


CMD ["ai_engine.app.handler"]
