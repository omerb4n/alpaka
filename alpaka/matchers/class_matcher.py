from typing import List, Optional, Union, ChainMap

from alpaka.apk.apk_info import ApkInfo
from alpaka.apk.class_info import ClassInfo
from alpaka.matchers.class_matches import ClassMatches, ClassMatch
from alpaka.matchers.classes_pool_matcher import ClassesPoolMatcher


class ClassMatcher:
    def __init__(self, old_apk_info: ApkInfo, new_apk_info: ApkInfo):
        self._old_apk_info = old_apk_info
        self._new_apk_info = new_apk_info
        self._classes_pool_matcher = ClassesPoolMatcher(self._old_apk_info, self._new_apk_info)
        self.class_matches = []

    def find_classes_matches(self) -> List[ClassMatches]:
        for classes_pool_match in self._classes_pool_matcher.pop_matched_packages_classes_pools():
            self._find_classes_matches_by_name(classes_pool_match.old_classes_pool, classes_pool_match.new_classes_pool)
        for all_classes_pool_match in self._classes_pool_matcher.get_all_classes_pool_chain_map():
            # TODO: uncomment the line bellow
            # classes_matches.append(self._find_class_matches_by_signature(class_info, classes_pool.new_classes))
            pass

    @staticmethod
    def _find_class_match_by_name(old_classes_pool: dict, new_classes_pool: dict, class_key) -> Optional[ClassMatch]:
        new_class: ClassInfo = new_classes_pool.get(class_key)
        if new_class.is_obfuscated_name:
            return None
        else:
            del old_classes_pool[class_key]
            del new_classes_pool[class_key]
            return ClassMatch(new_class, 1.0)

    def _find_classes_matches_by_name(self, old_classes_pool: dict, new_classes_pool: dict):
        for class_key in old_classes_pool:
            class_match = self._find_class_match_by_name(old_classes_pool, new_classes_pool, class_key)
            if class_match:
                self.class_matches.append(ClassMatches(old_classes_pool[class_key], [class_match]))

    def _find_classes_matches_by_signature(self, old_classes_pool: Union[dict, ChainMap],
                                           new_classes_pool: Union[dict, ChainMap]):
        pass

    def _find_class_matches_by_signature(self, class_to_match: ClassInfo,
                                         potential_matches: List[ClassInfo]) -> ClassMatches:
        # TODO: Use ClassSignature distances
        raise NotImplementedError()
