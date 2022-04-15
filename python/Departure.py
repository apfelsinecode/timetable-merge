from __future__ import annotations

import json
from datetime import datetime, timedelta

import requests
from bs4 import element, BeautifulSoup

from Stop import Stop
from StopSequence import StopSequence


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

            # date and time from linedata
            # date: '20220327' YYYYMMDD
            # time: '22:51' HH:mm
            self.datetime = datetime.strptime(
                self.line_data["date"] + "-" + self.line_data["time"],
                "%Y%m%d-%H:%M"
            )
            self.real_datetime = None
            if self.delay is not None:
                self.real_datetime = self.datetime + timedelta(minutes=int(self.delay))

            self.destination = td_destination.text.strip()
            self.platform = td_platform.text.strip()
        if len(trs) > 1:
            second_tr = trs[1]
            self.additional_info = [c.text for c in second_tr.children]

    def stop_sequence(self, use_realtime: bool = True, full_journey: bool = True) -> StopSequence:
        """
        request the stop sequence of this departure
        :param use_realtime:
        :param full_journey: show stops before current station
        :return:
        """
        return stop_sequence(linkdata=self.line_data,
                             line=self.line,
                             destination=self.destination,
                             use_realtime=use_realtime,
                             full_journey=full_journey
                             )

    def __str__(self) -> str:
        return f"{self.time} {self.delay if self.delay else ''} - {self.line} - {self.destination} - {self.platform}"

    def __repr__(self):
        return self.__str__()


def stop_sequence(linkdata: dict,
                  line: str,
                  destination: str,
                  use_realtime: bool = True,
                  full_journey: bool = True
                  ) -> StopSequence:
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

    return StopSequence(line, destination, stops_off + stops_on)
    # return stops_off + stops_on


stopseq_url = "https://www.bayern-fahrplan.de/xhr_stopseq_leg"
