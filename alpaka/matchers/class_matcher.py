import heapq
from typing import Optional

from alpaka.apk.apk_info import ApkInfo
from alpaka.apk.class_info import ClassInfo
from alpaka.class_signature.distance import WeightedSignatureDistanceCalculator, SignatureDistanceCalculator
from alpaka.config import MAXIMUM_SIGNATURE_MATCHES
from alpaka.matchers.class_matches import ClassMatches, ClassMatch
from alpaka.matchers.classes_matches import ClassesMatchesDict, ClassesMatches
from alpaka.matchers.classes_pool_match import ClassesPool
from alpaka.matchers.classes_pool_matcher import ClassesPoolMatcher


class ClassMatcher:
    """
    Responsible to find classes matches between two different apk infos.
    A class match is a match between a class in one apk to another class in the other apk.
    The match is done by class name or by similarities (signatue) between the classes.
    """

    def __init__(
            self,
            old_apk_info: ApkInfo,
            new_apk_info: ApkInfo,
            maximum_signature_matches=MAXIMUM_SIGNATURE_MATCHES,
            signature_distance_calculator: Optional[SignatureDistanceCalculator] = None,
    ):
        """
        Receives the two apk infos that their classes should be matched
        Before initializing the ClassMatcher, Filtering and packing the classes in both apks is recommend.
        :param old_apk_info: the older apk
        :param new_apk_info:
        """
        self._old_apk_info = old_apk_info
        self._new_apk_info = new_apk_info
        self._classes_pool_matcher = ClassesPoolMatcher(self._old_apk_info, self._new_apk_info)
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

    def find_classes_matches(self) -> ClassesMatches:
        """
        Iterates through all classes pools and tries to find matches by name:
            * First, iterate all matched packages classes pools and try to find matches:
                * by class name
                * then by signatures distance
            * Then try to find matches on all the remaining classes pool by signatures distance
        :return: ClassesMatches
        """
        self._classes_matches_dict = {}
        # For efficiency always use pop_matched_packages_classes_pools first
        for classes_pool_match in self._classes_pool_matcher.pop_matched_packages_classes_pools():
            self._find_classes_matches_by_name(classes_pool_match.old_classes_pool, classes_pool_match.new_classes_pool)
            self._find_classes_matches_by_signature(classes_pool_match.old_classes_pool,
                                                    classes_pool_match.new_classes_pool)
        all_classes_pool_match = self._classes_pool_matcher.get_all_classes_pool_chain_map()
        self._find_classes_matches_by_signature(all_classes_pool_match.old_classes_pool,
                                                all_classes_pool_match.new_classes_pool)
        return ClassesMatches(self._classes_matches_dict)

    @staticmethod
    def _find_class_match_by_name(new_classes_pool: dict, class_key) -> Optional[ClassMatch]:
        new_class: ClassInfo = new_classes_pool.get(class_key)
        if new_class is None or new_class.is_obfuscated_name:
            return None
        else:
            return ClassMatch(new_class, 1.0)

    def _find_classes_matches_by_name(self, old_classes_pool: dict, new_classes_pool: dict):
        """
        Finds classes matches by name and add the ClassMatches to self._classes_matches_dict
        Received classes pools will be filtered from matches thus, it's important they will be dicts and not ChainMaps.
        """
        if not (isinstance(old_classes_pool, dict) and isinstance(new_classes_pool, dict)):
            raise TypeError("classes_pool should be a dict")
        # Convert keys to list to avoid RuntimeError: dictionary changed size during iteration
        for class_key in list(old_classes_pool.keys()):
            class_match = self._find_class_match_by_name(new_classes_pool, class_key)
            if class_match:
                self._classes_matches_dict[class_key] = ClassMatches(old_classes_pool[class_key], [class_match])
                del old_classes_pool[class_key]
                del new_classes_pool[class_key]

    def _find_classes_matches_by_signature(self, old_classes_pool: ClassesPool,
                                           new_classes_pool: ClassesPool):
        """
        For each class in old_classes_pool find the closest classes in the new_classes_pool.
        Appends the found ClassMatches to self._classes_matches_dict
        """
        for old_class_info in old_classes_pool.values():
            old_class_signature = old_class_info.signature
            distances_per_class = (
                (new_class,
                 self._signature_distance_calculator.distance(old_class_signature, new_class.signature))
                for new_class in new_classes_pool.values())
            closest_distances_per_class = heapq.nsmallest(self._maximum_signature_matches, distances_per_class,
                                                          key=lambda distance_per_class: distance_per_class[1])

            self._classes_matches_dict[old_class_info.analysis.name] = ClassMatches(old_class_info, [
                ClassMatch(distance_per_class[0], distance_per_class[1]) for
                distance_per_class in closest_distances_per_class])
