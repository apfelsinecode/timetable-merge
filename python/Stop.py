from __future__ import annotations

from bs4 import element


class Stop:

    def __init__(self, as_string: str, station: str, arrival: str, departure: str, platform: str):
        self.as_string = as_string
        self.station = station
        self.arrival = arrival
        self.departure = departure
        self.platform = platform

    @staticmethod
    def from_tr(tr: element.Tag) -> Stop:
        as_string = tr.text.strip()
        tds = tr.find_all("td")
        td_station, td_arrival, td_departure, td_platform, *_ = tds
        station: str = td_station.text.strip()
        arrival: str = td_arrival.text.strip()
        departure: str = td_departure.text.strip()
        platform: str = td_platform.text.strip()
        return Stop(as_string, station, arrival, departure, platform)

    def __str__(self):
        return self.as_string

    def __repr__(self):
        return self.as_string

    def station_and_platform(self):
        return f"{self.station} {self.platform}"
