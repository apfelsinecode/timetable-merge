from __future__ import annotations

from datetime import datetime, timedelta, date, time
import matplotlib.pyplot as plt
import networkx as nx

import query_bayern_fahrplan as q
import timetable_merge as tm
from StopSequence import StopSequence


def next_saturday() -> datetime:
    today = date.today()
    # saturday is 5
    days_to_add = 7 + 5 - today.weekday()  # todo: test
    delta_to_add = timedelta(days=days_to_add)
    goal_time = time(0, 30)
    return datetime.combine(date=today + delta_to_add, time=goal_time)


def departures_next_saturday() -> list[q.Departure]:
    return q.departures_by_datetime(station_id=q.stations["Juliuspromenade"], dt=next_saturday())


def graph_saturday() -> nx.DiGraph:
    ds = departures_next_saturday()
    graph = tm.sequences_to_station_graph(
        sequences=[d.stop_sequence(full_journey=False).as_acyclic_stop_sequence() for d in ds]
    )
    return graph


def generate_graph_plot():
    graph = graph_saturday()
    fig, ax = plt.subplots()
    fig: plt.Figure
    ax: plt.Axes
    fig.set_size_inches(20, 20)
    nx.draw_networkx(graph, pos=nx.spring_layout(graph), ax=ax)
    fig.savefig("graph.png")


def main():
    generate_graph_plot()


if __name__ == '__main__':
    main()
