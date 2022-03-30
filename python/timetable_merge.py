from __future__ import annotations

import itertools
import subprocess

from StopSequence import StopSequence


def main():
    # subprocess.run([tsort], capture_output=True, text=True, input="a b\nc d")
    pass


def merge_stop_sequences(stop_sequences: list[StopSequence]):
    """
    use topological sort to generate a list of stops
    :param stop_sequences:
    :return:
    """
    pass


def topological_sort(pairs: list[(str, str)]) -> list[str]:
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


def sequence_to_pairs(sequence: list[str]) -> list[(str, str)]:
    return list(zip(sequence, itertools.islice(sequence, 1, None)))


if __name__ == '__main__':
    seq1 = [
        "Juliuspromenade",
        "Dom",
        "Rathaus",
        "Neubaustraße",
        "Sanderring",
        "Eichendorfstraße",
        "Königsberger Straße",
        "Reuterstraße",
        "Ostbahnhof",
        "Berner Straße",
    ]
    seq2 = [
        "Juliuspromenade",
        "Mainfranken Theater",
        "Berliner Ring",
        "Erthalstraße",
        "Hubland/Mensa",
        "Neue Universität",
        "Sanderring",
        "Königsberger Straße",
        "Reuterstraße",
        "Klingenstraße",
        "Berner Straße"
    ]
    seq3 = ["Busbahnhof", "Juliuspromenade"]
    elements = sequence_to_pairs(seq1) + sequence_to_pairs(seq2) + sequence_to_pairs(seq3)
    print(elements)
    _ordered = topological_sort(elements)
    print(_ordered)
