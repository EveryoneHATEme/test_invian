from datetime import datetime
from functools import wraps
from typing import Callable

from controller.analytics.allowed_signals import AllowedSignals


class DataAnalyser:
    def __init__(self) -> None:
        self.last_decision_datetime: datetime | None = None

    def analyze(self, data: list[tuple[int, int]]) -> AllowedSignals:
        pass
