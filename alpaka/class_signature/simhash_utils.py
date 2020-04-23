from typing import Iterable, Generator

# simhash-py package
import simhash


def calculate_simhash(tokens: Iterable[str]) -> int:
    return simhash.compute((
        simhash.unsigned_hash(bytes(token, 'utf-8'))
        for token in tokens
    ))


def calculate_distance(simhash1: int, simhash2: int):
    return simhash.num_differing_bits(simhash1, simhash2)


def calculate_shingle_simhash(tokens: Iterable, window: int = 4):
    """
    Calculate the simhash of token shingles.
    """
    return calculate_simhash(
        str(s)
        for s in shingle(tokens, window)
    )


def shingle(tokens: Iterable, window: int = 4) -> Generator[list, None, None]:
    """
    A generator for a moving window of the provided tokens.

    The shingle function from simhash-py 0.4.0 is broken in python 3.x.
    This is the shingle function taken from the newer
    versions of simhash-py, which were not uploaded to PYPI.
    """
    if window <= 0:
        raise ValueError("Window size must be positive")

    # Start with an empty output set.
    curr_window = []

    # Iterate over the input tokens, once.
    for token in tokens:
        # Add to the window.
        curr_window.append(token)

        # If we've collected too many, remove the oldest item(s) from the collection
        while len(curr_window) > window:
            curr_window.pop(0)

        # Finally, if the window is full, yield the data set.
        if len(curr_window) == window:
            yield list(curr_window)
