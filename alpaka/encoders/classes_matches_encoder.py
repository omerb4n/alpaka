from typing import Iterable, Mapping

from alpaka.apk.class_info import ClassInfo
from alpaka.matching.base import Match


def convert_class_matches_dict_to_output_format(matches_dict: Mapping[str, Iterable[Match[ClassInfo]]]):
    return {
        class_name: _convert_matches_to_output_format(class_matches)
        for class_name, class_matches in matches_dict.items()
    }


def _convert_matches_to_output_format(matches: Iterable[Match]):
    return {
        match.item2.analysis.name: match.match_rank
        for match in matches
    }
