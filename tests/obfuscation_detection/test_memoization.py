from unittest.mock import Mock

from alpaka.obfuscation_detection.memoization import MemoizingObfuscationDetector


def test_decorated_detector_called_one_time_per_identifier():

    decorated_detector = Mock()
    memoizing_detector = MemoizingObfuscationDetector(decorated_detector)

    memoizing_detector.is_class_name_obfuscated('Lcom/foo/bar/Baz;')
    decorated_detector.is_class_name_obfuscated.assert_called_once_with('Lcom/foo/bar/Baz;')
    memoizing_detector.is_class_name_obfuscated('Lcom/foo/bar/Baz;')
    memoizing_detector.is_class_name_obfuscated('Lcom/foo/bar/Baz;')
    decorated_detector.is_class_name_obfuscated.assert_called_once_with('Lcom/foo/bar/Baz;')

    memoizing_detector.is_class_name_obfuscated('Lanother/class/Identifier;')
    decorated_detector.is_class_name_obfuscated.assert_called_with('Lanother/class/Identifier;')
    assert decorated_detector.is_class_name_obfuscated.call_count == 2
    memoizing_detector.is_class_name_obfuscated('Lanother/class/Identifier;')
    memoizing_detector.is_class_name_obfuscated('Lanother/class/Identifier;')
    memoizing_detector.is_class_name_obfuscated('Lanother/class/Identifier;')
    assert decorated_detector.is_class_name_obfuscated.call_count == 2

    memoizing_detector.is_class_name_obfuscated('Lcom/foo/bar/Baz;')
    memoizing_detector.is_class_name_obfuscated('Lcom/foo/bar/Baz;')
    assert decorated_detector.is_class_name_obfuscated.call_count == 2

    memoizing_detector.is_class_name_obfuscated('Something')
    memoizing_detector.is_class_name_obfuscated('SomethingElse')
    memoizing_detector.is_class_name_obfuscated('Something')
    memoizing_detector.is_class_name_obfuscated('Lanother/class/Identifier;')
    memoizing_detector.is_class_name_obfuscated('Lcom/foo/bar/Baz;')
    assert decorated_detector.is_class_name_obfuscated.call_count == 4


def test_return_value_matches_decorated_detector():

    decorated_detector = Mock()
    decorated_detector.is_class_name_obfuscated.side_effect = lambda identifier: identifier
    memoizing_detector = MemoizingObfuscationDetector(decorated_detector)

    for i in range(4):
        assert memoizing_detector.is_class_name_obfuscated('Lcom/foo/bar/Baz;') == 'Lcom/foo/bar/Baz;'

    assert memoizing_detector.is_class_name_obfuscated('Lanother/class/Identifier;') == 'Lanother/class/Identifier;'
    assert memoizing_detector.is_class_name_obfuscated('Something') == 'Something'
    assert memoizing_detector.is_class_name_obfuscated('SomethingElse') == 'SomethingElse'
    assert memoizing_detector.is_class_name_obfuscated('Lcom/foo/bar/Baz;') == 'Lcom/foo/bar/Baz;'
    assert memoizing_detector.is_class_name_obfuscated('Lanother/class/Identifier;') == 'Lanother/class/Identifier;'
