import asyncio
from contextlib import asynccontextmanager
import json
from datetime import datetime
from time import time
from typing import Awaitable, Callable, AsyncGenerator
import sqlite3

from fastapi import FastAPI, Response, BackgroundTasks
from fastapi.responses import JSONResponse
from pytz import timezone

from controller.models import SensorDataModel
from controller.message_queue import Producer, Consumer
from controller.analytics import MeanThresholdAnalyser, AllowedSignals
from common import TCPServer, config


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Make required connections and setups before the application starts receiving requests
    :param _app:
    :return:
    """
    await consumer.connect()
    await producer.connect()
    task = asyncio.create_task(run_periodically(send_message_to_manipulator))
    await tcp_server.start()
    initialize_database()
    yield
    await consumer.disconnect()
    await producer.disconnect()
    task.cancel()
    await tcp_server.stop()
    database.close()


app = FastAPI(lifespan=lifespan)
consumer = Consumer()
producer = Producer()
tcp_server = TCPServer()
analytics = MeanThresholdAnalyser(threshold=1.0)
database = sqlite3.connect("manipulator_signals.db")


@app.post("/")
async def get_sensor_messages(
    sensor_data: SensorDataModel, background_tasks: BackgroundTasks
) -> Response:
    """
    API for sensors
    Sends received message to the RabbitMQ's queue
    :param sensor_data:
    :param background_tasks:
    :return: Empty response with code 200
    """
    background_tasks.add_task(producer.add_sensor_message, sensor_data)
    return Response()


@app.get("/history")
async def get_history(from_timestamp: int, to_timestamp: int) -> Response:
    cursor = database.cursor()
    cursor.execute(
        """
            SELECT timestamp, signal FROM signals_history
            WHERE timestamp BETWEEN ? AND ?
        """,
        (from_timestamp, to_timestamp),
    )
    result = cursor.fetchall()
    cursor.close()
    return JSONResponse(
        content=[
            {"timestamp": timestamp, "signal": signal} for timestamp, signal in result
        ]
    )


@app.get("/healthcheck")
async def get_healthcheck() -> Response:
    return Response("OK")


async def run_periodically(
    func: Callable[[], Awaitable[None]],
    period: int | float = config.MANIPULATOR_UPDATE_TIME,
) -> None:
    """
    Run given async function periodically with given period
    :param func:
    :param period:
    :return:
    """

    sleep_time = period
    try:
        while True:
            await asyncio.sleep(sleep_time)
            start_time = time()
            await func()
            time_taken = time() - start_time
            if time_taken >= period:
                sleep_time = 0.0
            else:
                sleep_time = period - time_taken
    except asyncio.CancelledError:
        pass


async def send_message_to_manipulator() -> None:
    """
    Send message to the manipulator using TCP connection
    Also saves message in database
    :return:
    """

    messages = await consumer.get_last_messages()
    status = analytics.analyze(messages)
    message_datetime = datetime.now(timezone("UTC"))

    message_to_send = json.dumps(
        {
            "datetime": message_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
            "status": status.value,
        }
    )
    add_signal_to_database(message_datetime.timestamp(), status)
    print(f"Sending message: {message_to_send}")

    await tcp_server.send_message(message_to_send)


def initialize_database() -> None:
    cursor = database.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS signals_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER,
            signal TEXT
        )
    """
    )
    database.commit()
    cursor.close()


def add_signal_to_database(timestamp: float | int, signal: AllowedSignals) -> None:
    cursor = database.cursor()
    cursor.execute(
        """
            INSERT INTO signals_history (timestamp, signal)
            VALUES (?, ?)
        """,
        (int(timestamp), signal.value),
    )
    database.commit()
    cursor.close()
