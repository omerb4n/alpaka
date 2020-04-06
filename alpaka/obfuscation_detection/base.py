import abc


class ObfuscationDetector(abc.ABC):
    def is_obfuscated(self, obj) -> bool:
        raise NotImplementedError()


class DummyObfuscationDetector(ObfuscationDetector):

    """
    A dummy obfuscation_detection detector, that declares anything as not obfuscated.
    Created for the POC
    """

    def is_obfuscated(self, obj) -> bool:
        return False