from __future__ import annotations

import collections
import itertools
import subprocess

from StopSequence import StopSequence
import query_bayern_fahrplan as q


def query_sample_stop_sequences(filter_destinations: list[str] = None):
    """
    generator function that calls departures function with default arguments and yields the stop sequence
    of each departure
    :return:
    """
    departures = q.departures()
    for departure in departures:
        if filter_destinations:
            if departure.destination in filter_destinations:
                yield departure.stop_sequence()
            else:
                print("wrong destination:", departure.destination)
        else:
            yield departure.stop_sequence()


def merge_sample_sequences():
    sequences = query_sample_stop_sequences(filter_destinations=["Sanderau", "Rottenbauer"])
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
    return topological_sort(pairs_flattened)


def topological_sort(pairs: collections.Iterable[(str, str)]) -> list[str]:
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


def main():
    # sequences = query_sample_stop_sequences(filter_destinations=["Sanderau", "Rottenbauer"])
    print(list(merge_sample_sequences()))
    # seq1 = [
    #     "Juliuspromenade",
    #     "Dom",
    #     "Rathaus",
    #     "Neubaustraße",
    #     "Sanderring",
    #     "Eichendorfstraße",
    #     "Königsberger Straße",
    #     "Reuterstraße",
    #     "Ostbahnhof",
    #     "Berner Straße",
    # ]
    # seq2 = [
    #     "Juliuspromenade",
    #     "Mainfranken Theater",
    #     "Berliner Ring",
    #     "Erthalstraße",
    #     "Hubland/Mensa",
    #     "Neue Universität",
    #     "Sanderring",
    #     "Königsberger Straße",
    #     "Reuterstraße",
    #     "Klingenstraße",
    #     "Berner Straße"
    # ]
    # seq3 = ["Busbahnhof", "Juliuspromenade"]
    # elements = sequence_to_pairs(seq1) + sequence_to_pairs(seq2) + sequence_to_pairs(seq3)
    # print(elements)
    # _ordered = topological_sort(elements)
    # print(_ordered)


if __name__ == '__main__':
    main()
