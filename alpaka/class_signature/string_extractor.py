from typing import Generator

from androguard.core.analysis.analysis import ClassAnalysis


class StringLiteralsExtractor:

    """
    This class extracts string literals out of class analysis objects.

    This class is based on androguard's create_xref method, which creates references from strings
    to the containing classes and methods, but not the other way for some reason
    """

    @classmethod
    def extract_strings(cls, class_analysis: ClassAnalysis) -> Generator[str, None, None]:
        for method in class_analysis.orig_class.get_methods():
            method_code = method.get_code()
            if method_code is None:
                continue

            for instruction in method_code.get_bc().get_instructions():
                op_value = instruction.get_op_value()

                # check for string literal instructions: const-string (0x1a), const-string/jumbo (0x1b)
                if 0x1a <= op_value <= 0x1b:
                    yield instruction.cm.vm.get_cm_string(instruction.get_ref_kind())
