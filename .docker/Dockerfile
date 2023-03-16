FROM python:3.10-slim

ENV PATH=/root/.poetry/bin:${PATH} \
    PIP_NO_CACHE_DIR=off \
    POETRY_VERSION=1.1.15 \
    POETRY_VIRTUALENVS_CREATE=false

RUN \
    apt-get update \
    && pip install -U pip \
    && pip install pipenv \
    && pip install "poetry==$POETRY_VERSION" \
    && pip3 install -U "poetry" \
    && rm -rf /var/lib/apt/lists

WORKDIR /app

COPY alembic.ini entrypoint.sh entrypoint-migrations.sh poetry.lock pyproject.toml ./
RUN poetry install

COPY assets ./assets
COPY bot ./bot
COPY common ./common
COPY migrations ./migrations

CMD ["sh", "entrypoint.sh"]
