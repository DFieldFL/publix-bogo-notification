from bs4 import BeautifulSoup, ResultSet
import requests


bogo_compare_text = [
    "buy 1 get 1 free",
    "buy one get one free",
    "buy one get 1 free",
    "buy 1 get one free",
]

b2g1_compare_text = [
    "buy 2 get 1 free",
    "buy two get one free",
    "buy 2 get one free",
    "buy two get 1 free",
]


def retrieve_sales_webpage(url: str) -> BeautifulSoup:
    """Retrieve sales webpage context as an BeautifulSoup object.

    Args:
        url (str): URL for retrieving the sales content

    Raises:
        Exception: Unseccessful status code returned
        Exception: No content was retrieved for the given URL

    Returns:
        BeautifulSoup: BeautifulSoup object containing the webpage content
    """
    response: requests.Response = requests.get(url, timeout=5)
    if response.status_code != 200:
        raise Exception("Unsuccessful status code returned")

    if not response.content:
        raise Exception("No content returned")

    return BeautifulSoup(response.content, "html.parser")


def parse_webpage_bogos(webpage_content: BeautifulSoup) -> list[(str, str)]:
    """Parse webpage content (BeautifulSoup) to find and return bogo items.

    Returns:
        list[(str, str)]: Tuple list of bogo items (<item name>, <bogo type>)
    """
    bogo_items = list[(str, str)]()

    webpage_items: ResultSet[any] = webpage_content.findAll(
        "div", attrs={"class": "theTileContainer"}
    )

    for item in webpage_items:
        item_deal_div: ResultSet[any] = item.find("div", attrs={"class": "deal"})

        # div could not be found so continue to the next item
        if item_deal_div is None:
            continue
        
        item_sale_text = item_deal_div.find(
            "span", attrs={"class": "ellipsis_text"}
        ).text
        is_bogo_text = bogo_text_type(item_sale_text)

        # save item and bogo type to the list of items to return
        if is_bogo_text:
            # Get item name
            item_name: str = (
                item.find("div", attrs={"class": "title"})
                .find("h2", attrs={"class": "ellipsis_text"})
                .text
            )
            bogo_items.append((item_name, is_bogo_text))

    return bogo_items


def bogo_text_type(item_sale_text: str) -> str | None:
    """Determine if sales text is a BOGO type sale or not.

    Args:
        item_sale_text (str): text to parse for BOGO type

    Returns:
        str: BOGO type text otherwise None
    """
    is_bogo_text = None

    if is_bogo(item_sale_text):
        is_bogo_text = "BOGO"
    elif is_b2g1(item_sale_text):
        is_bogo_text = "B2G1"

    return is_bogo_text


def is_bogo(item_sale_text: str) -> bool:
    """Determine if the sales text is for a BOGO sale.

    Args:
        item_sale_text (str): text to parse for BOGO

    Returns:
        bool: True if text is considered BOGO otherwise False
    """
    return is_text_in_list(item_sale_text, bogo_compare_text)


def is_b2g1(item_sale_text: str) -> bool:
    """Determine if the sales text is for a B2G1 sale.

    Args:
        item_sale_text (str): text to parse for B2G1

    Returns:
        bool: True if text is considered B2G1 otherwise False
    """
    return is_text_in_list(item_sale_text, b2g1_compare_text)

def is_text_in_list(text: str, compare_list: list[str]) -> bool:
    """Determine if text is in the compare list.

    This function is a case insensitive compare.

    Args:
        text (str): string to test against the compare list
        compare_list (list[str]): list of strings to compare the text against

    Returns:
        bool: true if text is in the compare list otherwise false
    """
    return any(s in text.lower() for s in compare_list)
