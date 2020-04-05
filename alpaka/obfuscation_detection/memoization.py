from alpaka.obfuscation_detection.base import ObfuscationDetector


class MemoizingObfuscationDetector(ObfuscationDetector):

    """
    A memoizing decorator for obfuscation_detection detectors.
    """

    def __init__(self, inner_detector: ObfuscationDetector):
        self._inner_detector = inner_detector
        self._detected_identifiers = dict()

    def is_obfuscated(self, obj) -> bool:
        if obj in self._detected_identifiers:
            return self._detected_identifiers[obj]
        result = self._inner_detector.is_obfuscated(obj)
        self._detected_identifiers[obj] = result
        return result
