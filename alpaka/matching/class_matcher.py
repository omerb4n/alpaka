import heapq
from typing import Optional

from alpaka.apk.class_pool import ClassPool
from alpaka.apk.class_info import ClassInfo
from alpaka.class_signature.distance import WeightedSignatureDistanceCalculator, SignatureDistanceCalculator
from alpaka.config import MAXIMUM_SIGNATURE_MATCHES
from alpaka.matching.class_matches import ClassMatches, ClassMatch
from alpaka.matching.classes_matches import ClassesMatchesDict, ClassesMatches


class ClassMatcher:
    """
    Responsible to find classes matches between two different class pools.
    A class match is a match between a class in one apk to another class in the other apk.
    The match is done by class name or by similarities (signature) between the classes.
    """

    def __init__(
            self,
            class_pool1: ClassPool,
            class_pool2: ClassPool,
            maximum_signature_matches=MAXIMUM_SIGNATURE_MATCHES,
            signature_distance_calculator: Optional[SignatureDistanceCalculator] = None,
            match_by_name: bool = True,
    ):
        self._class_pool1 = dict(class_pool1)
        self._class_pool2 = dict(class_pool2)
        self._classes_matches_dict: ClassesMatchesDict = {}
        if signature_distance_calculator is None:
            signature_distance_calculator = WeightedSignatureDistanceCalculator(
                member_count_weight=0.2,
                method_count_weight=0.2,
                instructions_count_weight=0.2,
                members_simhash_weight=0.1,
                methods_params_simhash_weight=0.1,
                methods_returns_simhash_weight=0.1,
                instructions_simhash_weight=0.1,
                instruction_shingles_simhash_weight=0.1,
                implemented_interfaces_count_weight=0.2,
                implemented_interfaces_simhash_weight=0.1,
                superclass_hash_weight=0.5,
                string_literals_count_weight=0.2,
                string_literals_simhash_weight=0.1,
            )
        self._signature_distance_calculator = signature_distance_calculator
        self._maximum_signature_matches = maximum_signature_matches
        self._match_by_name = match_by_name

    def find_classes_matches(self) -> ClassesMatches:
        """
        Iterates through all classes and tries to find matches by name:
        Then try to find matches on all the remaining classes pool by signatures distance
        :return: ClassesMatches
        """
        self._classes_matches_dict = {}
        if self._match_by_name:
            self._find_classes_matches_by_name()
        self._find_classes_matches_by_signature()
        return ClassesMatches(self._classes_matches_dict)

    @staticmethod
    def _find_class_match_by_name(class_pool: dict, class_key) -> Optional[ClassMatch]:
        new_class: ClassInfo = class_pool.get(class_key)
        if new_class is None or new_class.is_obfuscated_name:
            return None
        else:
            return ClassMatch(new_class, 1.0)

    def _find_classes_matches_by_name(self):
        """
        Finds classes matches by name and add the ClassMatches to self._classes_matches_dict
        Received classes pools will be filtered from matches thus, it's important they will be dicts and not ChainMaps.
        """
        # Convert keys to list to avoid RuntimeError: dictionary changed size during iteration
        for class_key in list(self._class_pool1.keys()):
            class_match = self._find_class_match_by_name(self._class_pool2, class_key)
            if class_match:
                self._classes_matches_dict[class_key] = ClassMatches(self._class_pool1[class_key], [class_match])
                del self._class_pool1[class_key]
                del self._class_pool2[class_key]

    def _find_classes_matches_by_signature(self):
        """
        For each class in old_classes_pool find the closest classes in the new_classes_pool.
        Appends the found ClassMatches to self._classes_matches_dict
        """
        for old_class_info in self._class_pool1.values():
            old_class_signature = old_class_info.signature
            distances_per_class = (
                (new_class,
                 self._signature_distance_calculator.distance(old_class_signature, new_class.signature))
                for new_class in self._class_pool2.values())
            closest_distances_per_class = heapq.nsmallest(self._maximum_signature_matches, distances_per_class,
                                                          key=lambda distance_per_class: distance_per_class[1])

            self._classes_matches_dict[old_class_info.analysis.name] = ClassMatches(old_class_info, [
                ClassMatch(distance_per_class[0], distance_per_class[1]) for
                distance_per_class in closest_distances_per_class])
