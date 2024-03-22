from pydantic_settings import BaseSettings


class Config(BaseSettings):
    CONTROLLER_HOST: str = '0.0.0.0'
    CONTROLLER_PORT: int = 8000
    CONTROLLER_URL: str = f'http://{CONTROLLER_HOST}:{CONTROLLER_PORT}'
    RABBITMQ_URL: str = 'amqp://guest:guest@localhost:5672/'
    RABBITMQ_EXCHANGE: str = 'sensor_data_exchange'
    RABBITMQ_QUEUE: str = 'sensor_data_queue'
    MANIPULATOR_WAIT_TIME: int = 5


config = Config()
