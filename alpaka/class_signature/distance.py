from abc import ABCMeta, abstractmethod

from alpaka.class_signature.signature import ClassSignature


class SignatureDistanceCalculator(metaclass=ABCMeta):

    @abstractmethod
    def distance(self, sig1: ClassSignature, sig2: ClassSignature) -> float:
        """
        Estimate the similarity of 2 classes based on their signature difference.

        :return: the distance between the signatures
        """
        raise NotImplementedError()


class WeightedSignatureDistanceCalculator(SignatureDistanceCalculator):

    def __init__(
            self,
            member_count_weight: float,
            method_count_weight: float,
            instructions_count_weight: float,
            members_simhash_weight: float,
            methods_params_simhash_weight: float,
            methods_returns_simhash_weight: float,
            instructions_simhash_weight: float,
    ):
        self.member_count_weight = member_count_weight
        self.instructions_count_weight = instructions_count_weight
        self.method_count_weight = method_count_weight
        self.members_simhash_weight = members_simhash_weight
        self.methods_params_simhash_weight = methods_params_simhash_weight
        self.methods_returns_simhash_weight = methods_returns_simhash_weight
        self.instructions_simhash_weight = instructions_simhash_weight

    def distance(self, sig1: ClassSignature, sig2: ClassSignature) -> float:
        return sum((
            self.member_count_weight * abs(sig2.member_count - sig1.member_count),
            self.method_count_weight * abs(sig2.method_count - sig1.method_count),
            self.instructions_count_weight * abs(sig2.instructions_count - sig1.instructions_count),
            self.members_simhash_weight * self._hamming_distance(sig1.members_simhash, sig2.members_simhash),
            self.methods_params_simhash_weight * self._hamming_distance(sig1.methods_params_simhash, sig2.methods_params_simhash),
            self.methods_returns_simhash_weight * self._hamming_distance(sig1.methods_returns_simhash, sig2.methods_returns_simhash),
            self.instructions_simhash_weight * self._hamming_distance(sig1.instructions_simhash, sig2.instructions_simhash),
        ))

    def _hamming_distance(self, str1, str2) -> int:
        """
        :return: the hamming distance between the 2 parameters
        """
        # todo: implement
        pass
