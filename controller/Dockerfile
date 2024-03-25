FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./controller /app/controller
COPY ./common /app/common

ENTRYPOINT ["python", "/app/controller/__main__.py"]
