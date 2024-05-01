from publix_bogos.bogos import BogoItem, BogoType
from publix_bogos.utils import is_any_whole_word_in_text


def filter_prettify_items(bogo_items: list[BogoItem], keywords: list[str], prefix: str, postfix: str) -> list[str]:
    """Filters bogo items to only the ones that match the keywords and adds the prefixing and postfixing.

    Args:
        bogo_items (list[BogoItem]): list of bogo items
        keywords (list[str]): keywords to filter bogo items
        prefix (str): prefix for bogo item text
        postfix (str): postfix for bogo item text

    Returns:
        list[str]: list of filtered bogo items that have prefixing and postfixing applied.
    """
    filtered_prettified_bogo_items = list[str]()
    for item in bogo_items:
        if is_any_whole_word_in_text(item.name, keywords):
            item_text = f'{item.name} is {item.type.value} {item.effective_dates}'
            if prefix:
                item_text = f'{prefix} {item_text}'

            if postfix:
                item_text = f'{item_text} {postfix}'

            filtered_prettified_bogo_items.append(item_text)

    return filtered_prettified_bogo_items
