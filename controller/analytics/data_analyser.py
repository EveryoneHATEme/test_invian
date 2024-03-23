from datetime import datetime
from functools import wraps
from typing import Callable

from controller.analytics.allowed_signals import AllowedSignals


class DataAnalyser:
    def __init__(self):
        self.last_decision_datetime: datetime | None = None

    def analyze(self, data: list[dict[str, int | str]]) -> AllowedSignals:
        pass

    def filter_outdated(
        self, data: list[dict[str, int | str]]
    ) -> list[dict[str, int | str]]:
        if self.last_decision_datetime is None:
            return data
        else:
            return [
                item
                for item in data
                if self.str_to_datetime(item["datetime"]) > self.last_decision_datetime
            ]

    def update_last_decision_datetime(self) -> None:
        self.last_decision_datetime = datetime.now()

    @staticmethod
    def str_to_datetime(string: str) -> datetime:
        return datetime.strptime(string, "%Y-%m-%dT%H:%M:%S")
