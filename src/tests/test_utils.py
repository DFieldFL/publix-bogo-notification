from publix_bogos.utils import is_any_in_text


def test_is_text_in_list():
    """Assert text is in list."""
    assert is_any_in_text("hello", ["bye", "hello"])


def test_is_text_in_list_case_insensetive():
    """Assert text is in list and it is not case sensitive."""
    assert is_any_in_text("HELLo", ["bye", "hello"])


def test_is_text_not_in_list():
    """Assert text is not in list."""
    assert not is_any_in_text("hi", ["bye", "hello"])
