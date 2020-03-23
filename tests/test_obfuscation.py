from alpaka.obfuscation import split_by_uppercase, calc_word_length_score, BAD_LENGTH, GREAT_LENGTH, is_obfuscated_word


def test_split_by_upper_case():
    assert split_by_uppercase("SignUp") == ["Sign", "Up"]
    assert split_by_uppercase("signUp") == ["sign", "Up"]


def test_get_word_length_score():
    assert calc_word_length_score("a" * BAD_LENGTH) == 0
    assert calc_word_length_score("a" * (BAD_LENGTH + 1)) > 0
    assert calc_word_length_score('a' * GREAT_LENGTH) == 1
    assert calc_word_length_score('a' * (GREAT_LENGTH + 1)) == 1


def test_is_obfuscated():
    assert is_obfuscated_word("asdff")
