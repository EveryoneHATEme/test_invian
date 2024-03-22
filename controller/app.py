import asyncio

from fastapi import FastAPI, Response, BackgroundTasks
import aio_pika

from models import SensorDataModel
from config import config
from message_queue import Producer, Consumer
from utils import repeat_every

app = FastAPI()
consumer = Consumer()
producer = Producer()


@app.on_event("startup")
async def start_queue():
    await consumer.connect()
    await producer.connect()


@app.post('/')
async def get_sensor_messages(sensor_data: SensorDataModel, background_tasks: BackgroundTasks) -> Response:
    background_tasks.add_task(producer.add_sensor_message, sensor_data)
    return Response()
