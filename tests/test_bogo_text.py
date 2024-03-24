from publix_bogos.bogos import is_bogo, is_text_in_list

def test_is_text_in_list():
    """Assert text is in list."""
    assert is_text_in_list("hello", ["bye", "hello"])


def test_is_text_in_list_case_insensetive():
    """Assert text is in list and it is not case sensitive."""
    assert is_text_in_list("HELLo", ["bye", "hello"])


def test_is_text_not_in_list():
    """Assert text is not in list."""
    assert not is_text_in_list("hi", ["bye", "hello"])


def test_bogo_text_upper_case():
    """Assert BOGO string with uppercase characters returns true."""
    assert is_bogo("BUY ONE GET ONE FREE")


def test_bogo_text_lower_case():
    """Assert BOGO string with lowercase characters returns true."""
    assert is_bogo("buy one get one free")


def test_bogo_text_mix_case():
    """Assert BOGO string with mixed case characters returns true."""
    assert is_bogo("bUy OnE gEt OnE fReE")


def test_bogo_text_not_bogo():
    """Assert non-BOGO string returns false."""
    assert not is_bogo("this is not bogo")
