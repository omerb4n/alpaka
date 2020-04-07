from androguard.core.bytecodes.dvm import Instruction

from alpaka.class_signature.class_signature_calculator import ClassSignatureCalculator
from alpaka.class_signature.simhash_utils import calculate_distance
from tests.conftest import mock_function


class DummyInstruction(Instruction):
    def get_name(self):
        return "dummy"


MAXIMUM_INSTRUCTIONS_TO_ADD_COUNT = 10


def test_calc_instructions_simhash(main_activity_class_fixture, monkeypatch):
    """
    Checks that instructions simhash distance is ascending when the difference in the instructions is ascending.
    :param main_activity_class_fixture:
    :param monkeypatch:
    :return:
    """
    original_instructions_simhash = ClassSignatureCalculator._calc_instructions_simhash(main_activity_class_fixture)
    original_function = ClassSignatureCalculator.iterate_class_instruction

    modified_simhash_distances = []
    instructions_to_add_count = [0]

    def mock_iterate_class_instruction(class_analysis):
        for instruction in original_function(class_analysis):
            yield instruction
        for _j in range(instructions_to_add_count[0]):
            yield DummyInstruction()

    mock_function(monkeypatch, ClassSignatureCalculator, ClassSignatureCalculator.iterate_class_instruction,
                  mock_iterate_class_instruction)

    for add_count in range(1, MAXIMUM_INSTRUCTIONS_TO_ADD_COUNT):
        instructions_to_add_count[0] = add_count
        modified_simhash_distances.append(calculate_distance(ClassSignatureCalculator._calc_instructions_simhash(
            main_activity_class_fixture), original_instructions_simhash))

    assert sorted(modified_simhash_distances) == modified_simhash_distances


def test_get_instructions_count(main_activity_class_fixture):
    assert ClassSignatureCalculator._get_instructions_count(main_activity_class_fixture) == 13
