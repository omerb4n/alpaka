from typing import Generator

from androguard.core.analysis.analysis import ClassAnalysis
from androguard.core.bytecodes.dvm import Instruction


def iterate_class_instruction(class_analysis: ClassAnalysis) -> Generator[Instruction, None, None]:
    for method in class_analysis.get_vm_class().get_methods():
        for instruction in method.get_instructions():
            yield instruction
