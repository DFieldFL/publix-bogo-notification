def is_any_in_text(text: str, compare_list: list[str]) -> bool:
    """Determine if any item in the compare list is in the text.

    This function is a case insensitive compare.

    Args:
        text (str): string to test
        compare_list (list[str]): list of strings to compare the text against

    Returns:
        bool: true if text is in the compare list otherwise false
    """
    return any(s in text.lower() for s in compare_list)


def is_any_whole_word_in_text(text: str, compare_list: list[str]) -> bool:
    """Determine if a whole word in the compare list is in the text.

    This function is a case insensitive compare.

    Args:
        text (str): string to test against
        compare_list (list[str]): list of strings to compare the text against

    Returns:
        bool: true if a whole word in the compare list is in the text, otherwise false
    """
    for text_substring in text.split(' '):
        if any(s == text_substring.lower() for s in compare_list):
            return True
    return False
