FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./sensors /app/sensors
COPY ./common /app/common

ENTRYPOINT ["python", "/app/sensors/__main__.py"]
