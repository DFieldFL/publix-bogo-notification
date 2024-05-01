from bs4 import BeautifulSoup, ResultSet
import requests
from enum import Enum

from publix_bogos.utils import is_any_in_text


class BogoType(Enum):
    NOBOGO = ''
    BOGO = 'BOGO'
    B2G1 = 'B2G1'


class BogoItem():
    def __init__(self, name: str, effective_dates: str, bogo_type: BogoType):
        """Initializes BOGO Item

        Args:
            name (str): Name of the BOGO item
            effective_dates (str): Effective dates of the BOGO item
            bogo_type (BogoType): Type of BOGO
        """
        self.name = name
        self.effective_dates = effective_dates
        self.type = bogo_type


bogo_compare_text = [
    'buy 1 get 1 free',
    'buy one get one free',
    'buy one get 1 free',
    'buy 1 get one free',
]

b2g1_compare_text = [
    'buy 2 get 1 free',
    'buy two get one free',
    'buy 2 get one free',
    'buy two get 1 free',
]


def retrieve_sales_webpage(url: str) -> BeautifulSoup:
    """Retrieve sales webpage context as an BeautifulSoup object.

    Args:
        url (str): URL for retrieving the sales content

    Raises:
        Exception: Unsuccessful status code returned
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


def parse_webpage_bogos(webpage_content: BeautifulSoup) -> list[BogoItem]:
    """Parse webpage content (BeautifulSoup) to find and return bogo items.

    Returns:
        list[BogoItem]]: List of bogo items
    """
    bogo_items = list[BogoItem]()

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
        bogo_type = get_bogo_type(item_sale_text)

        # save item and bogo type to the list of items to return
        if bogo_type != BogoType.NOBOGO:
            # Get item name
            item_name: str = (
                item.find("div", attrs={"class": "title"})
                .find("h2", attrs={"class": "ellipsis_text"})
                .text
            )
            effective_dates: str = (
                item.find("div", attrs={"class": "validDates"})
                .find("span")
                .text
            )
            bogo_items.append(BogoItem(item_name, effective_dates, bogo_type))

    return bogo_items


def get_bogo_type(item_sale_text: str) -> BogoType:
    """Determine if sales text is a BOGO type sale or not.

    Args:
        item_sale_text (str): text to parse for BOGO type

    Returns:
        BogoType: BOGO type
    """
    bogo_type = BogoType.NOBOGO

    if is_bogo(item_sale_text):
        bogo_type = BogoType.BOGO
    elif is_b2g1(item_sale_text):
        bogo_type = BogoType.B2G1

    return bogo_type


def is_bogo(item_sale_text: str) -> bool:
    """Determine if the sales text is for a BOGO sale.

    Args:
        item_sale_text (str): text to parse for BOGO

    Returns:
        bool: True if text is considered BOGO otherwise False
    """
    return is_any_in_text(item_sale_text, bogo_compare_text)


def is_b2g1(item_sale_text: str) -> bool:
    """Determine if the sales text is for a B2G1 sale.

    Args:
        item_sale_text (str): text to parse for B2G1

    Returns:
        bool: True if text is considered B2G1 otherwise False
    """
    return is_any_in_text(item_sale_text, b2g1_compare_text)
