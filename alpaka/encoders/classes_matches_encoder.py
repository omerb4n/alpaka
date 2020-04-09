from json import JSONEncoder

from alpaka.encoders.class_matches_encoder import ClassMatchesEncoder
from alpaka.matchers.class_matches import ClassMatches


class ClassesMatchesEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ClassMatches):
            return ClassMatchesEncoder.encode_class_matches(o)
        else:
            super(ClassesMatchesEncoder, self).default()
