FROM python:3.8.13-slim-buster

# set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true

ENV PATH="$POETRY_HOME/bin:$VIRTUAL_ENVIRONMENT_PATH/bin:$PATH"

# Install Poetry
# https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    build-essential \
    curl \
    && curl -sSL curl -sSL https://install.python-poetry.org | python3 -
    

WORKDIR /app
COPY ./pyproject.toml ./pyproject.toml
COPY ./poetry.lock ./poetry.lock
RUN poetry install --no-dev

COPY ./src/ /app/
COPY ./emoji_dataset.json /app/emoji_dataset.json

COPY ./start.sh /app/start.sh
RUN chmod +x /app/start.sh
CMD ./start.sh