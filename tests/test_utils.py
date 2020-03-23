from alpaka.utils import split_by_uppercase


def test_split_by_upper_case():
    assert split_by_uppercase("SignUp") == ["Sign", "Up"]
    assert split_by_uppercase("signUp") == ["Up"]
