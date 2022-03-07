
from __future__ import annotations
from bs4 import BeautifulSoup, element
import requests
import json

stopseq_url = "https://www.bayern-fahrplan.de/xhr_stopseq_leg"
departures_url = "https://www.bayern-fahrplan.de/de/abfahrt-ankunft/xhr_departures_fs"

stations = {
    "Würzburg": "80001152",
    "Busbahnhof": "80029081",
    "Juliuspromenade": "3700208",
    "Dom": "3700106",
    "Rathaus": "3700315",
    "Neubaustraße": "3700271",
    "Wirsbergstraße": "3700104",
    "Sanderring": "3700348",
    "Sanderglacisstraße": "3700346",
}


def get_departure_trs(station_id: str = stations["Sanderring"], date: str = None, time: str = None):
    """

    :param station_id:
    :param date: format DD.MM.YYYY
    :param time: format HH:MM
    :return:
    """
    params = {
        "is_fs": "1",
        "is_xhr": "True",
        "nameInfo_dm": station_id
    }
    if date:
        params["itdDateDayMonthYear"] = date
    if time:
        params["itdTime"] = time
    r = requests.get(departures_url, params=params)
    soup = BeautifulSoup(r.text, "html.parser")
    result = soup.find_all(attrs={"class": "results-tbody"})[0]
    return [c for c in result.children if (type(c) is element.Tag and c.name == "tr")]


def departures(station_id: str = stations["Sanderring"], date: str = None, time: str = None):
    ds = [Departure(c) for c in get_departure_trs(station_id, date, time)]
    return ds


class Departure:

    def __init__(self, tr: element.Tag):
        tbody = tr.find_all("tbody")[0]
        trs = [c for c in tbody.children if c.name == "tr"]
        first_tr: element.Tag = trs[0]
        if first_tr:
            tds = [c for c in first_tr.children if c.name == "td"]
            td_time_delay: element.Tag
            td_time_delay, td_line, td_destination, td_platform, *_ = tds

            # time and delay
            time_delay_spans = td_time_delay.find_all("span")
            self.delay = None
            if len(time_delay_spans) > 1:
                s_delay = time_delay_spans[1]
                self.delay = s_delay.text.strip()
            s_time = time_delay_spans[0]
            self.time = list(s_time.children)[0].text.strip()  # only first text child without nested delay span

            # line
            self.line = td_line.text.strip()  # td[1] includes mot in class-name
            a: element.Tag = td_line.find_all("a")[0]
            line_data_json = a["data-stopseq_linkdata"]
            self.line_data = json.loads(line_data_json)

            self.destination = td_destination.text.strip()
            self.platform = td_platform.text.strip()
        if len(trs) > 1:
            second_tr = trs[1]
            self.additional_info = [c.text for c in second_tr.children]

    def stop_sequence(self, use_realtime: bool = True, full_journey: bool = True):
        return stop_sequence(linkdata=self.line_data, use_realtime=use_realtime, full_journey=full_journey)

    def __str__(self) -> str:
        return f"{self.time} {self.delay if self.delay else ''} - {self.line} - {self.destination} - {self.platform}"


def stop_sequence(linkdata: dict, use_realtime: bool = True, full_journey: bool = True):
    params = linkdata.copy()
    if use_realtime:
        params["useRealtime"] = "1"
    if full_journey:
        params["tStOTType"] = "ALL"
    r = requests.get(stopseq_url, params=params)
    soup = BeautifulSoup(r.text, 'html.parser')
    trs_stops_off = soup.find_all(attrs={"class": "stops-off"})
    trs_stops_on = soup.find_all(attrs={"class": "stops-on"})
    stops_off = [Stop(tr) for tr in trs_stops_off]
    stops_on = [Stop(tr) for tr in trs_stops_on]

    return stops_off + stops_on


class Stop:

    def __init__(self, tr: element.Tag):
        self.as_string = tr.text.strip()
        tds = tr.find_all("td")
        td_station, td_arrival, td_departure, td_platform, *_ = tds
        self.station = td_station.text.strip()
        self.arrival = td_arrival.text.strip()
        self.departure = td_departure.text.strip()
        self.platform = td_platform.text.strip()

    def __str__(self):
        return self.as_string


if __name__ == '__main__':
    departures()
