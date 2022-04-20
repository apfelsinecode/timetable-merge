from __future__ import annotations

import copy
from collections import defaultdict
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

    def as_acyclic_stop_sequence(self) -> StopSequence:
        """

        :return: a new stop sequence where recurring stations are replaced with new stations with suffix #1, #2, ...
        """
        #  recurrence_counter = defaultdict(lambda x: 0)
        recurrence_counter = dict()
        new_stop_list = []
        for stop in self.stops:
            if stop.station in recurrence_counter.keys():
                # station occurred before
                prev_occurrences = recurrence_counter[stop.station]
                if prev_occurrences == 1:
                    # original still in list
                    original_stop = next((s for s in new_stop_list if s.station == stop.station))
                    original_stop.station += " #1"  # add number to station name
                new_stop = copy.copy(stop)
                recurrence_counter[stop.station] += 1
                new_stop.station += f" #{recurrence_counter[stop.station]}"
                new_stop_list.append(new_stop)
            else:
                # new previously unknown station
                recurrence_counter[stop.station] = 1
                new_stop_list.append(copy.copy(stop))
        return StopSequence(line=self.line, destination=self.destination, stops=new_stop_list)

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
