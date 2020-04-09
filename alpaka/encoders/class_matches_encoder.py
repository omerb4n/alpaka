from json import JSONEncoder

from alpaka.matchers.class_matches import ClassMatches


class ClassMatchesEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ClassMatches):
            self.encode_class_matches(o)
        else:
            super(ClassMatchesEncoder, self).default(o)

    @staticmethod
    def encode_class_matches(class_matches: ClassMatches):
        return {match.class_match.analysis.name: match.match_percentage for match in class_matches.matches}
