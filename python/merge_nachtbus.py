from __future__ import annotations

from datetime import datetime, timedelta, date, time
import matplotlib.pyplot as plt
import networkx as nx

import query_bayern_fahrplan as q
import timetable_merge as tm


def next_saturday() -> datetime:
    today = date.today()
    # saturday is 5
    current_weekday_plus_7 = today.weekday() + 7
    days_to_add = current_weekday_plus_7 - 2  # todo: fix
    delta_to_add = timedelta(days=days_to_add)
    goal_time = time(0, 0)
    return datetime.combine(date=today + delta_to_add, time=goal_time)


def departures_next_saturday() -> list[q.Departure]:
    return q.departures_by_datetime(station_id=q.stations["Juliuspromenade"], dt=next_saturday())


def generate_graph_plot():
    ds = departures_next_saturday()
    graph = tm.sequences_to_station_graph(sequences=[d.stop_sequence() for d in ds])
    fig, ax = plt.subplots()
    fig: plt.Figure
    ax: plt.Axes
    fig.set_size_inches(20, 20)
    nx.draw_networkx(graph, pos=nx.spring_layout(graph), ax=ax)
    fig.savefig("sample.png")


def main():
    generate_graph_plot()


if __name__ == '__main__':
    main()
