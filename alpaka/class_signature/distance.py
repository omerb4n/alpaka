from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

import simhash

from alpaka.class_signature.signature import ClassSignature
from alpaka.class_signature.simhash_utils import calculate_distance


class SignatureDistanceCalculator(metaclass=ABCMeta):

    @abstractmethod
    def distance(self, sig1: ClassSignature, sig2: ClassSignature) -> float:
        """
        Estimate the similarity of 2 classes based on their signature difference.

        :return: the distance between the signatures
        """
        raise NotImplementedError()


@dataclass(eq=False, order=False, frozen=True)
class WeightedSignatureDistanceCalculator(SignatureDistanceCalculator):

    member_count_weight: float
    method_count_weight: float
    instructions_count_weight: float
    members_simhash_weight: float
    methods_params_simhash_weight: float
    methods_returns_simhash_weight: float
    instructions_simhash_weight: float
    implemented_interfaces_count_wight: int
    implemented_interfaces_simhash_wight: int
    superclass_hash_wight: int

    def distance(self, sig1: ClassSignature, sig2: ClassSignature) -> float:
        return sum((
            self.member_count_weight * abs(sig2.member_count - sig1.member_count),
            self.method_count_weight * abs(sig2.method_count - sig1.method_count),
            self.instructions_count_weight * abs(sig2.instructions_count - sig1.instructions_count),
            self.members_simhash_weight * simhash.num_differing_bits(sig1.members_simhash, sig2.members_simhash),
            self.methods_params_simhash_weight * simhash.num_differing_bits(sig1.methods_params_simhash, sig2.methods_params_simhash),
            self.methods_returns_simhash_weight * simhash.num_differing_bits(sig1.methods_returns_simhash, sig2.methods_returns_simhash),
            self.instructions_simhash_weight * calculate_distance(sig1.instructions_simhash, sig2.instructions_simhash),
            self.implemented_interfaces_count_wight * abs(sig2.implemented_interfaces_count - sig1.implemented_interfaces_count),
            self.implemented_interfaces_simhash_wight * simhash.num_differing_bits(sig1.implemented_interfaces_simhash, sig2.implemented_interfaces_simhash),
            self.superclass_hash_wight if sig2.superclass_hash == sig1.superclass_hash else 0,
        ))
