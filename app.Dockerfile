FROM python:3.10-slim

ENV LISTEN_PORT=8000
EXPOSE 8000

RUN pip install poetry  
RUN mkdir -p /app  
COPY . /app

WORKDIR /app

RUN poetry install

CMD ["poetry", "run", "competency-analyser"]