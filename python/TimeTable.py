
from __future__ import annotations
# import pandas as pd
from StopSequence import StopSequence


class TimeTable:
    """
    a collection of stop sequences represented as a table
    """

    def __init__(self):
        self.stop_sequences: list[StopSequence] = list()
        self.stations: list[str] = list()
        # self.df = pd.DataFrame()

    def add_stop_sequence(self, stop_sequence: StopSequence):
        stations = [stop.station for stop in stop_sequence]
        self.stations += stations  # todo don't add if sequence is already present
        pass
