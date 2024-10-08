from __future__ import annotations

from abc import ABCMeta
from dataclasses import dataclass
from typing import TypeVar, Generic, Mapping, Tuple, Iterable

T = TypeVar('T')


class Matcher(Generic[T], metaclass=ABCMeta):

    def match(self, pool1: Mapping[str, T], pool2: Mapping[str, T]) -> MatchingResult[T]:
        raise NotImplementedError()


@dataclass
class Match(Generic[T]):
    item1: T
    item2: T
    match_rank: float


@dataclass
class MatchingResult(Generic[T]):
    matches: Mapping[str, Iterable[Match]]
    unmatched: Tuple[Mapping[str, T], Mapping[str, T]]

    def best_match(self, key):
        return min(self.matches[key], key=lambda m: m.match_rank)

    def best_matches(self):
        return (
            self.best_match(key)
            for key in self.matches.keys()
        )
