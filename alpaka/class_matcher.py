from typing import List

from alpaka.apk.apk_info import ApkInfo
from alpaka.apk.class_info import ClassInfo
from alpaka.apk.class_matches import ClassMatches, ClassMatch


class ClassMatcher:
    def __init__(self, old_apk_info: ApkInfo, new_apk_info: ApkInfo):
        self._old_apk_info = old_apk_info
        self._new_apk_info = new_apk_info

    def find_classes_matches(self) -> List[ClassMatches]:
        classes_matches: List[ClassMatches] = []
        for classes_pool in self._get_not_obfuscated_packages_classes_pools():
            for class_info in classes_pool.old_classes:
                if class_info.is_obfuscated_name:
                    pass
                else:
                    classes_matches.append(self._find_class_matches_by_name(class_info, classes_pool.new_classes))
        for classes_pool in self._get_classes_pools_iterator():
            for class_info in classes_pool.old_classes:
                if class_info.is_obfuscated_name:
                    # TODO: uncomment the line bellow
                    # classes_matches.append(self._find_class_matches_by_signature(class_info, classes_pool.new_classes))
                    pass
                else:
                    classes_matches.append(
                        self._find_class_matches_by_name(class_info, classes_pool.new_classes))
        return classes_matches

    def _find_class_matches_by_signature(self, class_to_match: ClassInfo,
                                         potential_matches: List[ClassInfo]) -> ClassMatches:
        # TODO: Use ClassSignature distances
        raise NotImplementedError()

    def _find_class_matches_by_name(self, class_to_match: ClassInfo,
                                    potential_matches: List[ClassInfo]) -> ClassMatches:
        # TODO: Maybe change ClassesPool.new_classes to be a dict
        #  so that finding the same class name will be more efficient
        for potential_match in potential_matches:
            if class_to_match.analysis.name == potential_match.analysis.name:
                # For efficiency. This will actually remove it from the classes_pool
                potential_matches.remove(potential_match)
                return ClassMatches(class_to_match, [ClassMatch(potential_match, 1.0)])
        return self._find_class_matches_by_signature(class_to_match, potential_matches)
