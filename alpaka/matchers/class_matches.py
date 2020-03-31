from dataclasses import dataclass
from typing import List

from alpaka.apk.class_info import ClassInfo


@dataclass
class ClassMatch:
    class_match: ClassInfo
    match_percentage: float


@dataclass
class ClassMatches:
    class_info: ClassInfo
    class_matches: List[ClassMatch]
