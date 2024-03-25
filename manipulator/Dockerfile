FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./manipulator /app/manipulator
COPY ./common /app/common

ENTRYPOINT ["python", "/app/manipulator/__main__.py"]
