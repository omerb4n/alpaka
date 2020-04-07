import abc


class ObfuscationDetector(abc.ABC):
    def is_obfuscated(self, obj) -> bool:
        raise NotImplementedError()


class DummyObfuscationDetector(ObfuscationDetector):
    """
    A dummy obfuscation detector, that declares anything as not obfuscated.
    Created for the POC
    """

    def __init__(self, is_obfuscated: bool):
        self._is_obfuscated: bool = is_obfuscated

    def is_obfuscated(self, obj) -> bool:
        return self._is_obfuscated
