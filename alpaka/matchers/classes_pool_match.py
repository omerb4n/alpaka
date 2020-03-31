from dataclasses import dataclass
from typing import ChainMap, Union

from alpaka.apk.class_info import ClassInfo
from alpaka.apk.package_info import ClassesDict

ClassesPool = Union[ClassesDict, ChainMap[str, ClassInfo]]


@dataclass
class ClassesPoolMatch:
    old_classes_pool: ClassesPool
    new_classes_pool: ClassesPool
