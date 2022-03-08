from __future__ import annotations

from typing import List, Tuple

from Stop import Stop


class StopSequence:

    def __init__(self, line: str, destination: str, stops: list[Stop]):  # add id: str as parameter here
        self.line = line
        self.destination = destination
        self.stops = stops

    def station_departure_list(self) -> List[Tuple[str, str]]:
        result = list()
        for stop in self.stops:
            result.append((stop.station, stop.departure))
        # result.sort(key=lambda pair: pair[1])  # order by departure time
        return result

    def station_arrival_list(self) -> List[Tuple[str, str]]:
        return [(stop.station, stop.arrival) for stop in self.stops]

    def station_departure_or_arrival_list(self) -> List[Tuple[str, str]]:
        """
        if no departure time is available, departure time is taken
        :return: list with tuples (station, time)
        """
        return [(stop.station, stop.departure or stop.arrival) for stop in self.stops]  # None or x -> x

    def __str__(self):
        return f"{self.line} {self.destination}: {str(self.stops)}"

    def __getitem__(self, item):
        return self.stops.__getitem__(item)

    def __len__(self):
        return self.stops.__len__()

    def __contains__(self, item):
        return self.stops.__contains__(item)

    def __iter__(self):
        return self.stops.__iter__()
