from operator import itemgetter

from controller.analytics.allowed_signals import AllowedSignals
from controller.analytics.data_analyser import DataAnalyser


class MeanThresholdAnalyser(DataAnalyser):
    def __init__(self, threshold: float = 0.0) -> None:
        super().__init__()
        self.threshold = threshold

    def analyze(self, data: list[dict[str, int | str]]) -> AllowedSignals:
        self.filter_outdated(data)
        mean_value = sum(map(itemgetter("payload"), data)) / len(data)
        self.update_last_decision_datetime()
        return AllowedSignals.UP if mean_value > self.threshold else AllowedSignals.DOWN
