import heapq
from typing import Optional, ChainMap

from alpaka.apk.class_pool import GlobalClassPool, ClassPool
from alpaka.apk.class_info import ClassInfo
from alpaka.apk.package_info import PackageInfo
from alpaka.class_signature.distance import WeightedSignatureDistanceCalculator, SignatureDistanceCalculator
from alpaka.config import MAXIMUM_SIGNATURE_MATCHES
from alpaka.matching.base import Match, MatchingResult
from alpaka.matching.class_matches import ClassMatches, ClassMatch
from alpaka.matching.classes_matches import ClassesMatchesDict, ClassesMatches
from alpaka.matching.package_matcher import NameBasedPackageMatcher


class ClassMatcher:
    """
    Responsible to find classes matches between two different apk infos.
    A class match is a match between a class in one apk to another class in the other apk.
    The match is done by class name or by similarities (signatue) between the classes.
    """

    def __init__(
            self,
            old_class_pool: GlobalClassPool,
            new_class_pool: GlobalClassPool,
            maximum_signature_matches=MAXIMUM_SIGNATURE_MATCHES,
            signature_distance_calculator: Optional[SignatureDistanceCalculator] = None,
            match_by_name: bool = True,
    ):
        """
        Receives the two apk infos that their classes should be matched
        Before initializing the ClassMatcher, Filtering and packing the classes in both apks is recommend.
        :param old_class_pool: the older apk
        :param new_class_pool:
        """
        self._old_class_pool = old_class_pool
        self._new_class_pool = new_class_pool
        self._package_matcher = NameBasedPackageMatcher()
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
        Iterates through all classes pools and tries to find matches by name:
            * First, iterate all matched packages classes pools and try to find matches:
                * by class name
                * then by signatures distance
            * Then try to find matches on all the remaining classes pool by signatures distance
        :return: ClassesMatches
        """
        self._classes_matches_dict = {}
        old_packages_dict = self._old_class_pool.split_by_package()
        new_packages_dict = self._new_class_pool.split_by_package()
        package_matching_result = self._package_matcher.match(old_packages_dict, new_packages_dict)
        for package_match in package_matching_result.best_matches():
            if self._match_by_name:
                self._find_classes_matches_by_name(package_match.item1, package_match.item2)
            self._find_classes_matches_by_signature(package_match.item1,
                                                    package_match.item2)
        all_classes_pool_match = self.get_remaining_classes_pool(package_matching_result)
        self._find_classes_matches_by_signature(all_classes_pool_match.item1,
                                                all_classes_pool_match.item2)
        return ClassesMatches(self._classes_matches_dict)

    @classmethod
    def get_remaining_classes_pool(cls, package_matching_result: MatchingResult[PackageInfo]) -> Match[ClassPool]:
        """
        Returns pools that hold all the remaining classes.

        For efficiency, each classes pool is a ChainMap.
        You should not remove elements or make any changes to this ChainMap.
        Changes will actually change the original dictionaries.
        :return: ClassesPoolMatch with pools that hold all the remaining classes
        """
        old_classes_chain_map = ChainMap(*package_matching_result.unmatched[0].values())
        new_classes_chain_map = ChainMap(*package_matching_result.unmatched[1].values())
        return Match(old_classes_chain_map, new_classes_chain_map, 0.0)

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

    def _find_classes_matches_by_signature(self, old_classes_pool: ClassPool,
                                           new_classes_pool: ClassPool):
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
