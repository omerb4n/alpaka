from dataclasses import dataclass
from typing import List

from alpaka.apk.class_info import ClassInfo


@dataclass
class ClassesPool:
    old_classes: List[ClassInfo]
    new_package: List[ClassInfo]
