qimport string

from alpaka.utils import split_by_separators


def test_split_by_separators():
    assert split_by_separators("SignUp", list(string.ascii_uppercase)) == ['Sign', 'Up']
    assert split_by_separators("helloFriend", list(string.ascii_uppercase)) == ["hello", "Friend"]
