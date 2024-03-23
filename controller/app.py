import asyncio
from contextlib import asynccontextmanager
import json
from datetime import datetime
from typing import Awaitable, Callable, AsyncGenerator

from fastapi import FastAPI, Response, BackgroundTasks

from controller.models import SensorDataModel
from controller.message_queue import Producer, Consumer
from controller.analytics import MeanThresholdAnalyser
from common import TCPServer


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    await consumer.connect()
    await producer.connect()
    task = asyncio.create_task(run_periodically(send_message_to_manipulator))
    await tcp_server.start()
    yield
    await consumer.disconnect()
    await producer.disconnect()
    task.cancel()
    await tcp_server.stop()


app = FastAPI(lifespan=lifespan)
consumer = Consumer()
producer = Producer()
tcp_server = TCPServer()
analytics = MeanThresholdAnalyser(threshold=1.0)


@app.post("/")
async def get_sensor_messages(
    sensor_data: SensorDataModel, background_tasks: BackgroundTasks
) -> Response:
    background_tasks.add_task(producer.add_sensor_message, sensor_data)
    return Response()


async def run_periodically(func: Callable[[], Awaitable[None]], period=5) -> None:
    try:
        while True:
            await asyncio.sleep(period)
            await func()
    except asyncio.CancelledError:
        pass


async def send_message_to_manipulator() -> None:
    messages = await consumer.get_last_messages()
    status = analytics.analyze(messages)
    message_to_send = json.dumps(
        {
            "datetime": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "status": status.name,
        }
    )
    await tcp_server.send_message(message_to_send)
