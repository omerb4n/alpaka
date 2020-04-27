import abc


class ObfuscationDetector(abc.ABC):

    def is_class_name_obfuscated(self, class_name) -> bool:
        raise NotImplementedError()

    def is_package_name_obfuscated(self, package_name) -> bool:
        raise NotImplementedError()


class DummyObfuscationDetector(ObfuscationDetector):
    """
    A dummy obfuscation detector, that declares anything as not obfuscated.
    Created for the POC
    """

    def __init__(self, is_obfuscated: bool):
        self._is_obfuscated: bool = is_obfuscated

    def is_class_name_obfuscated(self, class_name) -> bool:
        return self._is_obfuscated

    def is_package_name_obfuscated(self, package_name) -> bool:
        return self._is_obfuscated
