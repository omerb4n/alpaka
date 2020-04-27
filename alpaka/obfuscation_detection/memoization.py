from alpaka.obfuscation_detection.base import ObfuscationDetector


class MemoizingObfuscationDetector(ObfuscationDetector):

    """
    A memoizing decorator for obfuscation_detection detectors.
    """

    def __init__(self, inner_detector: ObfuscationDetector):
        self._inner_detector = inner_detector
        self._detected_classes = dict()
        self._detected_packages = dict()

    def is_class_name_obfuscated(self, class_name) -> bool:
        if class_name in self._detected_classes:
            return self._detected_classes[class_name]
        result = self._inner_detector.is_class_name_obfuscated(class_name)
        self._detected_classes[class_name] = result
        return result

    def is_package_name_obfuscated(self, package_name) -> bool:
        if package_name in self._detected_packages:
            return self._detected_packages[package_name]
        result = self._inner_detector.is_package_name_obfuscated(package_name)
        self._detected_packages[package_name] = result
        return result
