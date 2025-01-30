FROM python:3.11-slim-bullseye as builder

RUN pip install poetry

WORKDIR /usr

COPY ./poetry.lock ./pyproject.toml ./

RUN poetry config virtualenvs.in-project true --local && poetry install --only main

FROM python:3.11-slim-bullseye as compile-image

USER root

RUN apt-get update

WORKDIR /usr/public_api

COPY --from=builder /usr /usr
COPY . ./

ENV PATH="/usr/.venv/bin:$PATH"
ENV PYTHONPATH="/usr/public_api:$PYTHONPATH"
