from alpaka.obfuscation import WordObfuscationDetector


def test_word_obfuscation_detector():
    word_obfuscation_detector = WordObfuscationDetector()
    assert word_obfuscation_detector.is_obfuscated("asdff")
    assert not word_obfuscation_detector.is_obfuscated("hello")
    assert not word_obfuscation_detector.is_obfuscated("auth")
    assert not word_obfuscation_detector.is_obfuscated("maps")
