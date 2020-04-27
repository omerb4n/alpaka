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
    instruction_shingles_simhash_weight: float
    implemented_interfaces_count_weight: float
    implemented_interfaces_simhash_weight: float
    superclass_hash_weight: float
    string_literals_count_weight: float
    string_literals_simhash_weight: float

    @classmethod
    def from_weights_json(cls, weights_json):
        return cls(
            member_count_weight=weights_json['member_count'],
            method_count_weight=weights_json['method_count'],
            instructions_count_weight=weights_json['instructions_count'],
            members_simhash_weight=weights_json['members_simhash'],
            methods_params_simhash_weight=weights_json['methods_params_simhash'],
            methods_returns_simhash_weight=weights_json['methods_returns_simhash'],
            instructions_simhash_weight=weights_json['instructions_simhash'],
            instruction_shingles_simhash_weight=weights_json['instruction_shingles_simhash'],
            implemented_interfaces_count_weight=weights_json['implemented_interfaces_count'],
            implemented_interfaces_simhash_weight=weights_json['implemented_interfaces_simhash'],
            superclass_hash_weight=weights_json['superclass_hash'],
            string_literals_count_weight=weights_json['string_literals_count'],
            string_literals_simhash_weight=weights_json['string_literals_simhash'],
        )

    def distance(self, sig1: ClassSignature, sig2: ClassSignature) -> float:
        return sum((
            self.member_count_weight * abs(sig2.member_count - sig1.member_count),
            self.method_count_weight * abs(sig2.method_count - sig1.method_count),
            self.instructions_count_weight * abs(sig2.instructions_count - sig1.instructions_count),
            self.members_simhash_weight * simhash.num_differing_bits(sig1.members_simhash, sig2.members_simhash),
            self.methods_params_simhash_weight * simhash.num_differing_bits(sig1.methods_params_simhash, sig2.methods_params_simhash),
            self.methods_returns_simhash_weight * simhash.num_differing_bits(sig1.methods_returns_simhash, sig2.methods_returns_simhash),
            self.instructions_simhash_weight * calculate_distance(sig1.instructions_simhash, sig2.instructions_simhash),
            self.instruction_shingles_simhash_weight * calculate_distance(sig1.instruction_shingles_simhash, sig2.instruction_shingles_simhash),
            self.implemented_interfaces_count_weight * abs(sig2.implemented_interfaces_count - sig1.implemented_interfaces_count),
            self.implemented_interfaces_simhash_weight * simhash.num_differing_bits(sig1.implemented_interfaces_simhash, sig2.implemented_interfaces_simhash),
            self.superclass_hash_weight if sig2.superclass_hash != sig1.superclass_hash else 0,
            self.string_literals_count_weight * abs(sig2.string_literals_count - sig1.string_literals_count),
            self.string_literals_simhash_weight * simhash.num_differing_bits(sig1.string_literals_simhash, sig2.string_literals_simhash),
        ))
