from datetime import datetime
from time import sleep

import requests
from pytz import timezone

from sensors.generators import Generator, RandomGenerator
from common import config


class Sensor:
    def __init__(
        self,
        controller_address: str = config.CONTROLLER_URL,
        data_generator_cls: type[Generator] = RandomGenerator,
        timeout: float = 1.0 / config.SENSOR_REQUESTS_FREQUENCY,
    ) -> None:
        self.data_generator = data_generator_cls()

        self.controller_address = controller_address
        self.session = requests.Session()
        self.payload = {"datetime": "", "payload": 0}
        self.timeout = timeout

    def __del__(self) -> None:
        self.session.close()

    def send(self, payload: int) -> None:
        self.payload["datetime"] = datetime.now(timezone("UTC")).strftime(
            "%Y-%m-%dT%H:%M:%S"
        )
        self.payload["payload"] = payload

        try:
            self.session.post(
                url=self.controller_address, json=self.payload, timeout=self.timeout
            )
        except requests.exceptions.Timeout:
            # print("Request timed")
            return
        except requests.exceptions.ConnectionError:
            sleep(1)

    def start(self) -> None:
        self.loop()

    def loop(self) -> None:
        while True:
            read_data = self.data_generator.generate()
            self.send(read_data)
