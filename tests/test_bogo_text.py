from publix_bogos.bogos import is_bogo


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
