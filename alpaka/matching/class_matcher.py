import heapq

from alpaka.apk.class_info import ClassInfo
from alpaka.apk.class_pool import ClassPool
from alpaka.class_signature.distance import WeightedSignatureDistanceCalculator, SignatureDistanceCalculator
from alpaka.config import MAXIMUM_SIGNATURE_MATCHES
from alpaka.matching.base import Matcher, MatchingResult, Match


class ClassMatcher(Matcher[ClassInfo]):
    """
    Responsible to find classes matches between two different class pools.
    A class match is a match between a class in one apk to another class in the other apk.
    The match is done by class name or by similarities (signature) between the classes.
    """

    def __init__(
            self,
            maximum_matches_per_class=MAXIMUM_SIGNATURE_MATCHES,
            signature_distance_calculator: SignatureDistanceCalculator = None
    ):
        self.maximum_matches_per_class = maximum_matches_per_class
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

    def match(self, pool1: ClassPool, pool2: ClassPool, match_by_name: bool = True) -> MatchingResult[ClassInfo]:
        """
        Iterates through all classes and tries to find matches by name
        Then try to find matches on all the remaining classes pool by signatures distance
        """
        pool1 = dict(pool1)
        pool2 = dict(pool2)
        class_matches = dict()
        if match_by_name:
            class_matches.update(self._match_by_name(pool1, pool2))
        class_matches.update(self._match_by_signature(pool1, pool2))
        return MatchingResult(class_matches, (dict(), dict()))

    @classmethod
    def _match_by_name(cls, pool1, pool2):
        class_matches = dict()
        # Convert keys to list to avoid RuntimeError: dictionary changed size during iteration
        for class_key, class_info in list(pool1.items()):
            if class_info.is_obfuscated_name:
                continue
            matching_class = pool2.get(class_key)
            if matching_class is None or matching_class.is_obfuscated_name:
                continue
            class_matches[class_key] = [(Match(class_info, matching_class, 1.0))]
            del pool1[class_key]
            del pool2[class_key]
        return class_matches

    def _match_by_signature(self, pool1, pool2):
        """
        For each class in old_classes_pool find the closest classes in the new_classes_pool.
        """
        class_matches = dict()
        for class_name, class_info in pool1.items():
            distances_per_class = {
                possible_match:
                    self._signature_distance_calculator.distance(class_info.signature, possible_match.signature)
                for possible_match in pool2.items()
            }
            closest_distances_per_class = heapq.nsmallest(
                self.maximum_matches_per_class,
                distances_per_class.items(),
                key=lambda distance_per_class: distance_per_class[1]
            )

            class_matches[class_name] = [
                Match(class_info, matching_class, distance)
                for matching_class, distance in closest_distances_per_class
            ]
        return class_matches
