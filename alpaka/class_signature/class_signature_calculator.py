from androguard.core.analysis.analysis import ClassAnalysis

from alpaka.class_signature.signature import ClassSignature
from alpaka.class_signature.simhash_utils import calculate_simhash


class ClassSignatureCalculator:

    def calculate_class_signature(self, class_analysis: ClassAnalysis) -> ClassSignature:
        return ClassSignature(
            member_count=self._get_member_count(class_analysis),
            method_count=self._get_method_count(class_analysis),
            instructions_count=self._get_instructions_count(class_analysis),
            members_simhash=self._calc_members_simhash(class_analysis),
            methods_params_simhash=self._calc_methods_params_simhash(class_analysis),
            method_returns_simhash=self._calc_methods_returns_simhash(class_analysis),
            instructions_simhash=self._calc_instructions_simhash(class_analysis),
        )

    @classmethod
    def _get_member_count(cls, class_analysis: ClassAnalysis) -> int:
        return len(class_analysis.get_fields())

    @classmethod
    def _get_method_count(cls, class_analysis: ClassAnalysis) -> int:
        return class_analysis.get_nb_methods()

    @classmethod
    def _get_instructions_count(cls, class_analysis: ClassAnalysis):
        raise NotImplementedError()

    @classmethod
    def _calc_members_simhash(cls, class_analysis: ClassAnalysis) -> int:
        return calculate_simhash((
            member.field.get_descriptor()
            for member in class_analysis.get_fields()
        ))

    @classmethod
    def _calc_methods_params_simhash(cls, class_analysis: ClassAnalysis):
        raise NotImplementedError()

    @classmethod
    def _calc_methods_returns_simhash(cls, class_analysis: ClassAnalysis):
        raise NotImplementedError()

    @classmethod
    def _calc_instructions_simhash(cls, class_analysis: ClassAnalysis):
        raise NotImplementedError()
