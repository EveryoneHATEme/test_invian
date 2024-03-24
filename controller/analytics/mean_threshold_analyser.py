from operator import itemgetter

from controller.analytics.allowed_signals import AllowedSignals
from controller.analytics.data_analyser import DataAnalyser


class MeanThresholdAnalyser(DataAnalyser):
    def __init__(self, threshold: float = 0.0) -> None:
        super().__init__()
        self.threshold = threshold

    def analyze(self, data: list[tuple[int, int]]) -> AllowedSignals:
        if data:
            mean_value = sum(map(itemgetter(1), data)) / len(data)
        else:
            mean_value = 0.0
        print(f"{mean_value=}")
        return AllowedSignals.UP if mean_value > self.threshold else AllowedSignals.DOWN
