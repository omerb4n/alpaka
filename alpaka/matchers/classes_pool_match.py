from dataclasses import dataclass
from typing import ChainMap, Union

ClassesPool = Union[dict, ChainMap]


@dataclass
class ClassesPoolMatch:
    old_classes_pool: ClassesPool
    new_classes_pool: ClassesPool
