from dataclasses import dataclass

from alpaka.apk.class_pool import ClassPool


@dataclass
class ClassesPoolMatch:
    old_classes_pool: ClassPool
    new_classes_pool: ClassPool
