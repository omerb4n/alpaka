import pytest
from androguard.core.analysis.analysis import ClassAnalysis

from alpaka.class_signature.class_signature_calculator import ClassSignatureCalculator


@pytest.fixture(scope='function')
def main_activity_class_fixture(hello_apk_classes_fixture) -> ClassAnalysis:
    return hello_apk_classes_fixture["Lcom/example/myapplication/MainActivity;"]


def test_calc_instructions_simhash(main_activity_class_fixture):
    ClassSignatureCalculator._calc_instructions_simhash(main_activity_class_fixture)
