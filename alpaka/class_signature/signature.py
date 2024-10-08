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
    instruction_shingles_simhash: int
    implemented_interfaces_count: int
    implemented_interfaces_simhash: int
    superclass_hash: int
    string_literals_count: int
    string_literals_simhash: int
