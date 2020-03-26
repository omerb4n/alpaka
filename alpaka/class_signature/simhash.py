from typing import Iterable

import simhash


def calculate_simhash(tokens: Iterable[str]) -> int:
    return simhash.compute((
        simhash.unsigned_hash(bytes(token))
        for token in tokens
    ))