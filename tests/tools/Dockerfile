FROM python:3.11-slim-bullseye

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

RUN pip install poetry

WORKDIR /usr/bot

RUN git clone https://github.com/Dmitriy1101/test_telegramm_bot.git .

RUN git pull origin main

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-root

ENV PATH="/usr/.venv/bin:$PATH"
