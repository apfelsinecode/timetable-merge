from __future__ import annotations

import collections
import itertools
import subprocess
import networkx as nx
from matplotlib import pyplot as plt
from typing import Callable

from StopSequence import StopSequence
import query_bayern_fahrplan as q


def query_sample_stop_sequences(filter_departures: Callable[[q.Departure], bool] = lambda x: True):
    """
    generator function that calls departures function with default arguments and yields the stop sequence
    of each departure
    :return:
    """
    departures = q.departures()
    for departure in departures:
        if filter_departures(departure):
            yield departure.stop_sequence()
        else:
            print("wrong departure:", departure)


def merge_sample_sequences():
    def _filter(d: q.Departure):
        return d.destination in ["Sanderau" "Rottenbauer"]
    sequences = query_sample_stop_sequences(filter_departures=_filter)
    return merge_stop_sequences(sequences)


def merge_stop_sequences(stop_sequences: collections.Iterable[StopSequence]) -> collections.Iterable[str]:
    """
    use topological sort to generate a list of stops
    :param stop_sequences:
    :return:
    """
    station_lists: collections.Iterable[list[str]]\
        = [[stop.station_and_platform() for stop in sequence.stops] for sequence in stop_sequences]
    # use station and platform because line 4 stops twice at Juliuspromenade but at different platforms
    half_ordering_pairs = (sequence_to_pairs(station_list) for station_list in station_lists)
    pairs_flattened = itertools.chain(*half_ordering_pairs)
    return topological_sort_old(pairs_flattened)


def topological_sort_old(pairs: collections.Iterable[(str, str)]) -> list[str]:
    """
    calls command tsort to sort topologically

    spaces in input strings will be replaced by "***" while calculating
    :param pairs: pairs of strings indicating the given partial ordering
    :return: total ordering of the strings
    """
    input_string = ""
    for first, second in pairs:
        first: str
        second: str
        first = first.replace(" ", "***")
        second = second.replace(" ", "***")
        input_string += f"{first} {second}\n"

    tsort = subprocess.run(["tsort"], capture_output=True, text=True, input=input_string, check=True)
    ordered = tsort.stdout
    return [word.replace("***", " ") for word in ordered.splitlines()]


def sequence_to_pairs(sequence: collections.Iterable[str]) -> collections.Iterable[(str, str)]:
    return zip(sequence, itertools.islice(sequence, 1, None))


def sequences_to_station_graph(sequences: collections.Iterable[StopSequence]) -> nx.DiGraph:
    graph = nx.DiGraph()
    for sequence in sequences:
        nx.add_path(graph, [it.station for it in sequence])
    return graph


def sequences_to_acyclic_station_graph(sequences: collections.Iterable[StopSequence]) -> nx.DiGraph:
    """
    if a sequence contains
    :param sequences:
    :return:
    """
    return sequences_to_station_graph((s.as_acyclic_stop_sequence() for s in sequences))


def topologically_sorted_stations(sequences: collections.Iterable[StopSequence]) -> collections.Iterable[str]:
    """use this as index for dataframes"""
    graph = sequences_to_acyclic_station_graph(sequences)
    return nx.topological_sort(graph)


def main():
    def _filter(d: q.Departure):
        return d.destination in ["Sanderau", "Rottenbauer"]
    sequences = query_sample_stop_sequences(filter_departures=_filter)
    graph = sequences_to_station_graph(sequences)
    nx.draw_networkx(graph)
    plt.show()
    # print(list(merge_sample_sequences()))


if __name__ == '__main__':
    main()
