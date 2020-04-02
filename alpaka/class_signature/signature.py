from dataclasses import dataclass


@dataclass
class ClassSignature:
    member_count: int
    method_count: int
    instructions_count: int
    members_simhash: int
    methods_params_simhash: int
    methods_returns_simhash: int
    instructions_simhash: int
