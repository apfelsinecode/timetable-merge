from __future__ import annotations

import collections
from datetime import datetime, timedelta

from bs4 import BeautifulSoup, element
import requests

from Departure import Departure

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


def get_departure_trs_and_last_departure_date_time(
        station_id: str = stations["Sanderring"],
        date: str = None,
        time: str = None
) -> (collections.Iterable[element.Tag], str, str):
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
    last_departure_time = soup.find("input", attrs={'class': 'last_departure_time'}).attrs['value']
    last_departure_date = soup.find("input", attrs={'class': 'last_departure_date'}).attrs['value']
    print(last_departure_date, last_departure_time)
    return (c for c in result.children if (type(c) is element.Tag and c.name == "tr")), \
        last_departure_date, last_departure_time


def departures(station_id: str = stations["Sanderring"], date: str = None, time: str = None)\
        -> (collections.Iterable[Departure], str, str):
    """
    :param station_id: see stations dict
    :param date: format DD.MM.YYYY (%d.%m.%Y)
    :param time: format HH:MM (%H:%M)
    :return Departure objects, last departure date in format %d.%m.%Y, last departure time %H:%M
    """
    trs, last_departure_date, last_departure_time =\
        get_departure_trs_and_last_departure_date_time(station_id, date, time)
    ds = (Departure(c) for c in trs)
    return ds, last_departure_date, last_departure_time


def only_departures(station_id: str = stations["Sanderring"], date: str = None, time: str = None)\
        -> collections.Iterable[Departure]:
    return departures(station_id, date, time)[0]


def departures_by_datetime(station_id: str = stations["Sanderring"], dt: datetime = None)\
        -> (collections.Iterable[Departure], str, str):
    print("request for", dt)
    if dt:
        return departures(station_id=station_id, date=dt.strftime("%d.%m.%Y"), time=dt.strftime("%H:%M"))
    else:
        return departures(station_id=station_id)


def departures_by_datetime_range(
        station_id: str = stations["Sanderring"],
        start: datetime | None = None,
        end: datetime | timedelta | None = None) -> collections.Generator[Departure, None, None]:
    """
    calls departure_by_datetime multiple times until end time is reached

    this function is a generator-function to potentially limit the number of useless API requests

    if start is not given, the start of the range is now (no date or time will be passed)

    if end is not given, the result contains departures from exactly one request (same as using
    departures_by_datetime directly)

    :param station_id: the station id (same as in other methods)
    :param start: the initial time for the first request
    :param end: the end of the desired range (exclusive); can also be a timedelta, that will be added to start
    :return: a generator of all departures that are within the range from start (inclusive) to end (exclusive)
    """
    # TODO no_cutoff argument: yield all departures from the last request even if they are after specified end
    if start is None and end is not None:
        _start: datetime = datetime.now()
    else:
        _start: datetime | None = start

    if type(end) == timedelta:  # implies that end is not None
        _end: datetime = _start + end
    else:
        _end: datetime | None = end

    current_datetime = _start
    while _end is None or current_datetime < _end:
        ds, last_date, last_time = departures_by_datetime(station_id, current_datetime)
        for d in ds:
            if _end is None or d.datetime < _end:
                yield d
        current_datetime = datetime.strptime(f"{last_date} {last_time}", "%d.%m.%Y %H:%M")
        if _end is None:
            break  # run loop exactly once if no end is given


if __name__ == '__main__':
    _d = departures_by_datetime_range(start=datetime(2022, 4, 23, 0, 15), end=datetime(2022, 4, 23, 5, 0))
    try:
        while True:
            input()
            print(next(_d), end='')
    except StopIteration:
        print("done")
