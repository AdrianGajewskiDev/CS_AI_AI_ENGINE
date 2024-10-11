FROM python:3.12.4-alpine
WORKDIR ${LAMBDA_TASK_ROOT}

COPY ./ai_engine ${LAMBDA_TASK_ROOT}/ai_engine
COPY ./pyproject.toml ${LAMBDA_TASK_ROOT}
COPY ./poetry.lock ${LAMBDA_TASK_ROOT}
COPY ./README.md ${LAMBDA_TASK_ROOT}

RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

CMD ["ai_engine.app.handler"]
