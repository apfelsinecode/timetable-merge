import math

import query_bayern_fahrplan as q
from datetime import datetime, timedelta


def main():
    departures = q.only_departures()
    now = datetime.now()
    for departure in departures:
        time_diff = (departure.real_datetime or departure.datetime) - now
        display_time: str
        if time_diff > timedelta(minutes=15):
            if departure.real_datetime:
                display_time = f"{departure.time} {departure.delay} {departure.real_datetime.strftime('%H:%M')}"
            else:
                display_time = departure.time
        else:
            display_time = f"'{math.floor(time_diff.seconds / 60)}"
            if departure.real_datetime:
                display_time += f" ({departure.time} {departure.delay} {departure.real_datetime.strftime('%H:%M')})"
        print(departure.line, departure.destination, display_time, sep="\t")


if __name__ == '__main__':
    main()
