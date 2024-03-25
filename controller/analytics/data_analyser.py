from abc import ABC, abstractmethod

from controller.analytics.allowed_signals import AllowedSignals


class DataAnalyser(ABC):
    """
    Abstract method for data analysers
    To make data analyser inherit from this class and implement the analyze method
    """

    @abstractmethod
    def analyze(self, data: list[tuple[int, int]]) -> AllowedSignals:
        pass
