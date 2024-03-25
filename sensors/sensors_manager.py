from multiprocessing import Process

from sensors.sensor import Sensor
from common import config


class SensorsManager:
    """
    Manager used to test the project locally
    Creates given amount of sensors and processes for each sensor
    """

    def __init__(
        self,
        number_of_sensors: int = 8,
        sensor_request_timeout: float = 1.0 / 300,
        controller_address: str = config.CONTROLLER_URL,
    ) -> None:
        self.sensor_request_timeout = sensor_request_timeout
        self.controller_address = controller_address

        self.sensors = [
            Sensor(self.controller_address, timeout=self.sensor_request_timeout)
            for _ in range(number_of_sensors)
        ]
        self.processes = [Process(target=sensor.start()) for sensor in self.sensors]

    def start(self) -> None:
        for process in self.processes:
            process.start()

    def stop(self) -> None:
        for sensor, process in zip(self.sensors, self.processes):
            del sensor
            process.join()
