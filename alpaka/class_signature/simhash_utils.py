from typing import Iterable

import simhash


def calculate_simhash(tokens: Iterable[str]) -> int:
    return simhash.compute((
        simhash.unsigned_hash(bytes(token, 'utf-8'))
        for token in tokens
    ))


def calculate_distance(simhash1: int, simhash2: int):
    return simhash.num_differing_bits(simhash1, simhash2)
