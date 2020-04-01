import heapq
from typing import List, Optional

from alpaka.apk.apk_info import ApkInfo
from alpaka.apk.class_info import ClassInfo
from alpaka.class_signature.distance import WeightedSignatureDistanceCalculator
from alpaka.matchers.class_matches import ClassMatches, ClassMatch
from alpaka.matchers.classes_pool_match import ClassesPool
from alpaka.matchers.classes_pool_matcher import ClassesPoolMatcher

NUMBER_OF_CLASSES_TO_FIND_BY_SIGNATURE = 3


class ClassMatcher:
    def __init__(self, old_apk_info: ApkInfo, new_apk_info: ApkInfo):
        self._old_apk_info = old_apk_info
        self._new_apk_info = new_apk_info
        self._classes_pool_matcher = ClassesPoolMatcher(self._old_apk_info, self._new_apk_info)
        self.class_matches = []
        self._weighted_signature_distance_calculator = WeightedSignatureDistanceCalculator(0.2, 0.2, 0.2, 0.1, 0.1, 0.1,
                                                                                           0.1)

    def find_classes_matches(self):
        # For efficiency always use pop_matched_packages_classes_pools first
        for classes_pool_match in self._classes_pool_matcher.pop_matched_packages_classes_pools():
            self._find_classes_matches_by_name(classes_pool_match.old_classes_pool, classes_pool_match.new_classes_pool)
            self._find_classes_matches_by_signature(classes_pool_match.old_classes_pool,
                                                    classes_pool_match.new_classes_pool)
        all_classes_pool_match = self._classes_pool_matcher.get_all_classes_pool_chain_map()
        self._find_classes_matches_by_signature(all_classes_pool_match.old_classes_pool,
                                                all_classes_pool_match.new_classes_pool)

    @staticmethod
    def _find_class_match_by_name(new_classes_pool: dict, class_key) -> Optional[ClassMatch]:
        new_class: ClassInfo = new_classes_pool.get(class_key)
        if new_class is None or new_class.is_obfuscated_name:
            return None
        else:
            return ClassMatch(new_class, 1.0)

    def _find_classes_matches_by_name(self, old_classes_pool: dict, new_classes_pool: dict):
        """
        Received classes pools will be filtered from matches thus, it's important they will be dicts.
        :param old_classes_pool:
        :param new_classes_pool:
        :return:
        """
        if not (isinstance(old_classes_pool, dict) and isinstance(new_classes_pool, dict)):
            raise TypeError("classes_pool should be a dict")
        # Convert keys to list to avoid RuntimeError: dictionary changed size during iteration
        for class_key in list(old_classes_pool.keys()):
            class_match = self._find_class_match_by_name(new_classes_pool, class_key)
            if class_match:
                self.class_matches.append(ClassMatches(old_classes_pool[class_key], [class_match]))
                del old_classes_pool[class_key]
                del new_classes_pool[class_key]

    def _find_classes_matches_by_signature(self, old_classes_pool: ClassesPool,
                                           new_classes_pool: ClassesPool):
        """
        For each class in old_classes_pool find the closest classes in the new_classes_pool.
        Appends the found ClassMatches to self.class_matches
        :param old_classes_pool:
        :param new_classes_pool:
        :return:
        """
        for old_class_info in old_classes_pool.values():
            old_class_signature = old_class_info.signature
            distances_per_class = (
                (new_class,
                 self._weighted_signature_distance_calculator.distance(old_class_signature, new_class.signature))
                for new_class in new_classes_pool.values())
            closest_distances_per_class = heapq.nsmallest(NUMBER_OF_CLASSES_TO_FIND_BY_SIGNATURE, distances_per_class,
                                                          key=lambda distance_per_class: distance_per_class[1])

            self.class_matches.append(ClassMatches(old_class_info,
                                                   [ClassMatch(distance_per_class[0], distance_per_class[1]) for
                                                    distance_per_class in closest_distances_per_class]))
