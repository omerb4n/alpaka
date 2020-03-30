from typing import List

from alpaka.apk.apk_info import ApkInfo
from alpaka.apk.class_info import ClassInfo
from alpaka.matchers.class_matches import ClassMatches, ClassMatch
from alpaka.matchers.classes_pool_matcher import ClassesPoolMatcher


class ClassMatcher:
    def __init__(self, old_apk_info: ApkInfo, new_apk_info: ApkInfo):
        self._old_apk_info = old_apk_info
        self._new_apk_info = new_apk_info
        self._classes_pool_matcher = ClassesPoolMatcher(self._old_apk_info, self._new_apk_info)

    def find_classes_matches(self) -> List[ClassMatches]:
        classes_matches: List[ClassMatches] = []
        for classes_pool_match in self._classes_pool_matcher.pop_matched_packages_classes_pools():
            for class_key in classes_pool_match.old_classes_pool:
                new_class = classes_pool_match.new_classes_pool.get(class_key)
                if new_class.is_obfuscated_name:
                    pass
                else:
                    old_class = classes_pool_match.old_classes_pool.pop(class_key)
                    del classes_pool_match.new_classes_pool[class_key]
                    classes_matches.append(ClassMatches(old_class, [new_class]))
        all_classes_pool = self._classes_pool_matcher.get_all_classes_pool()
        for class_info in all_classes_pool.old_classes_pool:
            # TODO: uncomment the line bellow
            # classes_matches.append(self._find_class_matches_by_signature(class_info, classes_pool.new_classes))
            pass
        return classes_matches

    def _find_class_matches_by_signature(self, class_to_match: ClassInfo,
                                         potential_matches: List[ClassInfo]) -> ClassMatches:
        # TODO: Use ClassSignature distances
        raise NotImplementedError()
