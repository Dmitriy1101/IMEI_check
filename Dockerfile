FROM python:3.11-slim-bullseye 

USER root

RUN apt-get update

RUN pip install poetry

WORKDIR /usr

COPY ./poetry.lock ./pyproject.toml ./

RUN poetry config virtualenvs.in-project true --local && poetry install --only main

COPY . ./

ENV PATH="/usr/.venv/bin:$PATH"
