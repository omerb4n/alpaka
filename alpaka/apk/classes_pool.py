from dataclasses import dataclass
from typing import List

from alpaka.apk.class_info import ClassInfo


@dataclass
class ClassesPoolMatch:
    old_classes_pool: List[ClassInfo]
    new_classes_pool: List[ClassInfo]
