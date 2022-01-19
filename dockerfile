from python:3.8.10 as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
RUN pip install poetry

COPY .env alembic.ini main.py poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-dev

COPY alembic alembic
COPY db db
COPY src src

FROM base as build
CMD alembic upgrade head && python3 main.py

FROM base as test
COPY tests tests
RUN pip install poetry
RUN poetry install
CMD poetry run pytest --cov=app tests/
