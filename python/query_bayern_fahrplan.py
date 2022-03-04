
from __future__ import annotations
from bs4 import BeautifulSoup, element
import requests

stopseq_url = "https://www.bayern-fahrplan.de/xhr_stopseq_leg"
departures_url = "https://www.bayern-fahrplan.de/de/abfahrt-ankunft/xhr_departures_fs"

stations = {
    "Würzburg": "80001152",
    "Busbahnhof": "80029081",
    "Sanderring": "3700348",
}


def get_trs(station_id: str = stations["Sanderring"]):
    params = {
        "is_fs": "1",
        "is_xhr": "True",
        # "incl_mot5": "1",
        "nameInfo_dm": station_id
    }
    r = requests.get(departures_url, params=params)
    soup = BeautifulSoup(r.text, "html.parser")
    result = soup.find_all(attrs={"class": "results-tbody"})[0]
    return [c for c in result.children if (type(c) is element.Tag and c.name == "tr")]


def departures(station_id: str = stations["Sanderring"]):
    ds = [Departure(c) for c in get_trs(station_id)]
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

            time_delay_spans = td_time_delay.find_all("span")
            self.delay = None
            if len(time_delay_spans) > 1:
                s_delay = time_delay_spans[1]
                self.delay = s_delay.text.strip()
            s_time = time_delay_spans[0]
            self.time = list(s_time.children)[0].text.strip()  # only first text child without nested delay span

            self.line = tds[1].text.strip()  # td[1] includes mot in class-name
            self.destination = tds[2].text.strip()
            self.platform = tds[3].text.strip()
        if len(trs) > 1:
            second_tr = trs[1]
            self.additional_info = [c.text for c in second_tr.children]

    def __str__(self) -> str:
        return f"{self.time} {self.delay if self.delay else ''} - {self.line} - {self.destination} - {self.platform}"


if __name__ == '__main__':
    departures()
