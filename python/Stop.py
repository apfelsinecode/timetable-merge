from __future__ import annotations

from bs4 import element


class Stop:

    def __init__(self, tr: element.Tag):
        self.as_string = tr.text.strip()
        tds = tr.find_all("td")
        td_station, td_arrival, td_departure, td_platform, *_ = tds
        self.station: str = td_station.text.strip()
        self.arrival: str = td_arrival.text.strip()
        self.departure: str = td_departure.text.strip()
        self.platform: str = td_platform.text.strip()

    def __str__(self):
        return self.as_string

    def __repr__(self):
        return self.as_string

    def station_and_platform(self):
        return f"{self.station} {self.platform}"
