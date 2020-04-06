from unittest.mock import MagicMock, Mock

from alpaka.obfuscation_detection.simple_detection import SimpleObfuscationDetector
import pytest


@pytest.mark.parametrize(('value', 'expected_result'), (
    ('primitive', False),
    ('not_both_versions', True),
    ('external', False),
    ('correct_words', False),
    ('something_else', True),
))
def test_is_obfuscated(value, expected_result):
    detector = SimpleObfuscationDetector(Mock(), Mock(), Mock())
    detector._is_primitive = Mock(side_effect=lambda x: x == 'primitive')
    detector._is_in_both_versions = Mock(side_effect=lambda x: x != 'not_both_versions')
    detector._is_external = Mock(side_effect=lambda x: x == 'external')
    detector._is_all_correct_words = Mock(side_effect=lambda x: x == 'correct_words')

    assert detector.is_obfuscated(value) == expected_result


def test_is_all_correct_words():
    dictionary = MagicMock()
    detector = SimpleObfuscationDetector(Mock(), Mock(), dictionary)
    detector._separate_class_descriptor_to_words = Mock(return_value=['Foo', 'Bar', 'Baz'])

    dictionary.__contains__.return_value = True
    assert detector._is_all_correct_words('')

    dictionary.__contains__.return_value = False
    assert not detector._is_all_correct_words('')

    dictionary.__contains__.side_effect = lambda word: word == 'Foo'
    assert not detector._is_all_correct_words('')
    dictionary.__contains__.side_effect = lambda word: word != 'Baz'
    assert not detector._is_all_correct_words('')


@pytest.mark.parametrize(('string', 'expected_words'), (
    ('LFooBar;', ['Foo', 'Bar']),
    ('LfooBar;', ['foo', 'Bar']),
    ('LFooBarBaz;', ['Foo', 'Bar', 'Baz']),
    ('LUPPERCASESomething;', ['UPPERCASE', 'Something']),
    ('LCamelCaseUPPERCASECamelCase;', ['Camel', 'Case', 'UPPERCASE', 'Camel', 'Case']),
    ('LAtTheEndThereWillBeUPPERCASE;', ['At', 'The', 'End', 'There', 'Will', 'Be', 'UPPERCASE']),
    ('Lwords-with_Special/Characters$between=them+CamelCase;', ['words', 'with', 'Special', 'Characters', 'between', 'them', 'Camel', 'Case']),
    ('Lwords5with543numbers;', ['words', 'with', 'numbers']),
))
def test_separate_class_descriptor_to_words(string, expected_words):
    assert SimpleObfuscationDetector._separate_class_descriptor_to_words(string) == expected_words
