from dataclasses import dataclass
from typing import ChainMap, Union


@dataclass
class ClassesPoolMatch:
    old_classes_pool: Union[dict, ChainMap]
    new_classes_pool: Union[dict, ChainMap]
