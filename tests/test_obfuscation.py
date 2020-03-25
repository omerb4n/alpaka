from alpaka.obfuscation.obfuscation import WordObfuscationDetector, ClassNameObfuscationDetector, \
    PackageNameObfuscationDetector


def test_word_obfuscation_detector():
    word_obfuscation_detector = WordObfuscationDetector()
    assert word_obfuscation_detector.is_obfuscated("asdff")
    assert not word_obfuscation_detector.is_obfuscated("hello")
    assert not word_obfuscation_detector.is_obfuscated("auth")
    assert not word_obfuscation_detector.is_obfuscated("maps")


def test_class_name_obfuscation_detector():
    is_obfuscated_func = ClassNameObfuscationDetector().is_obfuscated
    assert is_obfuscated_func("ABC")
    # assert is_obfuscated_func("ABCD")
    assert is_obfuscated_func("C099602p")
    assert is_obfuscated_func("AnonymosClass1MQ")
    assert is_obfuscated_func("AnonymosClass123")
    assert is_obfuscated_func("anonymosclass123")
    assert not is_obfuscated_func("hellofriend")
    # assert is_obfuscated_func("sdfgsjkosfsd")
    assert not is_obfuscated_func("NativePeer")
    assert not is_obfuscated_func("ResultReceiver")
    assert not is_obfuscated_func("IResultReceiver")
    # assert not is_obfuscated_func("IValue")
    assert is_obfuscated_func("R")


def test_package_name_obfuscation_detector():
    is_obfuscated_func = PackageNameObfuscationDetector().is_obfuscated
    assert not is_obfuscated_func("hello")
    assert not is_obfuscated_func("hello_friend")
    assert not is_obfuscated_func("hi_bye")
    assert is_obfuscated_func("asdsgd")
    assert is_obfuscated_func("asd123")
    assert is_obfuscated_func("dfhgdifhsdvn")
