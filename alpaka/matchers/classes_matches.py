from typing import Dict

from alpaka.matchers.class_matches import ClassMatches

ClassesMatchesDict = Dict[str, ClassMatches]


class ClassesMatches:
    def __init__(self, classes_matches_dict: ClassesMatchesDict = None):
        if not classes_matches_dict:
            self.classes_matches_dict = {}
        else:
            self.classes_matches_dict = classes_matches_dict
