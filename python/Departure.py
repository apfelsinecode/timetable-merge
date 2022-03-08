from __future__ import annotations

import json

from bs4 import element

from query_bayern_fahrplan import stop_sequence


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
        return stop_sequence(linkdata=self.line_data,
                             line=self.line,
                             destination=self.destination,
                             use_realtime=use_realtime,
                             full_journey=full_journey
                             )

    def __str__(self) -> str:
        return f"{self.time} {self.delay if self.delay else ''} - {self.line} - {self.destination} - {self.platform}"