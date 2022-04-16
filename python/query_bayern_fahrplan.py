
from __future__ import annotations

from datetime import datetime

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
    """
    :param station_id: see stations dict
    :param date: format DD.MM.YYYY (%d.%m.%Y)
    :param time: format HH:MM (%H:%M)
    """
    ds = [Departure(c) for c in get_departure_trs(station_id, date, time)]
    return ds


def departures_by_datetime(station_id: str = stations["Sanderring"], dt: datetime = None):
    if dt:
        return departures(station_id=station_id, date=dt.strftime("%d.%m.%Y"), time=dt.strftime("%H:%M"))
    else:
        return departures(station_id=station_id)


def stops_as_dataframe(stops):  # -> pd.DataFrame:
    data = {}  # index is column, value is list of row elements per column; column represent
    for stop in stops:
        pass
    pass


if __name__ == '__main__':
    d = departures()
    _stops = d[0].stop_sequence()
