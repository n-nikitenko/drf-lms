FROM python:3.8.1

ENV POETRY_VERSION=1.8.2
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

RUN python3 -m venv $POETRY_VENV \
	&& $POETRY_VENV/bin/pip install -U pip setuptools \
	&& $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /code

COPY pyproject.toml ./

RUN poetry install --no-interaction --no-ansi

COPY config ./config

COPY materials ./materials

COPY fixtures ./fixtures

COPY users ./users

COPY manage.py ./



