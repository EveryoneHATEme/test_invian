from pydantic_settings import BaseSettings


class Config(BaseSettings):
    CONTROLLER_IP: str = "0.0.0.0"
    CONTROLLER_HTTP_PORT: int = 8000
    CONTROLLER_URL: str = f"http://{CONTROLLER_IP}:{CONTROLLER_HTTP_PORT}"
    CONTROLLER_TCP_PORT: int = 8888
    MANIPULATOR_WAIT_TIME: int = 5
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"
    RABBITMQ_EXCHANGE: str = "sensor_data_exchange"
    RABBITMQ_QUEUE: str = "sensor_data_queue"


config = Config()
