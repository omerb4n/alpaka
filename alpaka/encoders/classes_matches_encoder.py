from json import JSONEncoder

from alpaka.matching.class_matches import ClassMatches
from alpaka.matching.classes_matches import ClassesMatches


class ClassesMatchesEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ClassMatches):
            return self.encode_class_matches(o)
        if isinstance(o, ClassesMatches):
            return self.encode_classes_matches(o)
        super(ClassesMatchesEncoder, self).default(o)

    @staticmethod
    def encode_classes_matches(classes_matches: ClassesMatches):
        return classes_matches.classes_matches_dict

    @staticmethod
    def encode_class_matches(class_matches: ClassMatches):
        return {match.class_match.analysis.name: match.match_percentage for match in class_matches.matches}
