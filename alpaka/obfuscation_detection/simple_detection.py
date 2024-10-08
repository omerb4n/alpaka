import re
from typing import List

import enchant
from androguard.core.analysis.analysis import Analysis

from alpaka.obfuscation_detection.base import ObfuscationDetector


class SimpleObfuscationDetector(ObfuscationDetector):

    """
    A simple obfuscation_detection detector, based on multiple checks which can either return a result or
    fallback to the next check.
    This detector is built to be relatively quick, while providing a low false-negative percentage.
    false-positive errors don't affect the signature accuracy as much, and this detector is built with that goal in mind.
    """

    WORD_REGEX = re.compile(r'(?:[A-Z](?=[^a-z]|$))+|[a-zA-Z][a-z]*')

    def __init__(self, old_analysis: Analysis, new_analysis: Analysis, dictionary: enchant.Dict = enchant.Dict('en_US')):
        self._old_analysis = old_analysis
        self._new_analysis = new_analysis
        self._dictionary = dictionary

    def is_class_name_obfuscated(self, class_name) -> bool:
        class_name = class_name.lstrip('[')
        if self._is_primitive(class_name): return False
        if not self._is_in_both_versions(class_name): return True
        if self._is_external(class_name): return False
        if self._is_all_correct_words(class_name): return False
        return True

    def is_package_name_obfuscated(self, package_name) -> bool:
        return not self._is_all_correct_words(package_name)

    @classmethod
    def _is_primitive(cls, class_descriptor: str) -> bool:
        return class_descriptor in {'V', 'Z', 'B', 'S', 'C', 'I', 'J', 'F', 'D'}

    def _is_in_both_versions(self, class_descriptor: str) -> bool:
        return self._old_analysis.is_class_present(class_descriptor) \
               and self._new_analysis.is_class_present(class_descriptor)

    def _is_external(self, class_descriptor: str) -> bool:
        if class_descriptor.startswith('Landroid/') or class_descriptor.startswith('Ljava/'):
            return True
        # todo: need to check if the above is correct (maybe non-external android/ classes can be defined by the developer?)
        return self._new_analysis.get_class_analysis(class_descriptor).is_external()

    def _is_all_correct_words(self, class_descriptor):
        return all(
            len(word) >= 2 and self._dictionary.check(word)
            for word in self._separate_class_descriptor_to_words(class_descriptor)
        )

    @classmethod
    def _separate_class_descriptor_to_words(cls, class_descriptor: str) -> List[str]:
        return cls.WORD_REGEX.findall(class_descriptor, pos=1)
