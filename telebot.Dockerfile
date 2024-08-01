FROM python:3.10-slim

ENV LISTEN_PORT=7999
EXPOSE 7999

RUN pip install poetry
RUN mkdir -p /telegram_app
COPY . /telegram_app

WORKDIR /telegram_app

RUN poetry install
CMD ["poetry", "run", "competency-analyser-telegram-bot"]