from bs4 import BeautifulSoup, ResultSet
import requests


def retrieve_bogos(config) -> list[str]:
    """TODO

    Args:
        config (_type_): _description_

    Returns:
        list[str]: _description_
    """
    sales_content: BeautifulSoup = retrieve_sales_webpage(config["url"])
    return parse_webpage_bogos(sales_content)


def retrieve_sales_webpage(url: str) -> BeautifulSoup:
    """Retrieve sales webpage context as an BeautifulSoup object.

    Args:
        url (str): URL for retrieving the sales content

    Raises:
        Exception: Unseccessful status code returned
        Exception: None content was retrieved for the given URL

    Returns:
        BeautifulSoup: BeautifulSoup object containing the webpage content
    """
    response: requests.Response = requests.get(url, timeout=5)
    if response.status_code != 200:
        raise Exception("Unsuccessful status code returned")

    if not response.content:
        raise Exception("No content returned")

    return BeautifulSoup(response.content, "html.parser")


def parse_webpage_bogos(webpage_content: BeautifulSoup) -> list[str]:
    bogo_items = list[str]()

    webpage_items: ResultSet[any] = webpage_content.findAll(
        "div", attrs={"class": "theTileContainer"}
    )

    for item in webpage_items:
        item_name: str = (
            item.find("div", attrs={"class": "title"})
            .find("h2", attrs={"class": "ellipsis_text"})
            .text
        )
        item_deal_div: ResultSet[any] = item.find("div", attrs={"class": "deal"})
        if item_deal_div is None:
            continue
        item_sale_text = item_deal_div.find(
            "span", attrs={"class": "ellipsis_text"}
        ).text

        is_bogo_text = bogo_text_type(item_sale_text)

        if is_bogo_text:
            bogo_items.append(is_bogo_text)

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
    bogo_text = [
        "buy 1 get 1 free",
        "buy one get one free",
        "buy one get 1 free",
        "buy 1 get one free",
    ]
    return any(s in item_sale_text.lower() for s in bogo_text)


def is_b2g1(item_sale_text: str) -> bool:
    """Determine if the sales text is for a B2G1 sale.

    Args:
        item_sale_text (str): text to parse for B2G1

    Returns:
        bool: True if text is considered B2G1 otherwise False
    """

    b2g1_text = [
        "buy 2 get 1 free",
        "buy two get one free",
        "buy 2 get one free",
        "buy two get 1 free",
    ]
    return any(s in item_sale_text.lower() for s in b2g1_text)


# def find_items():


class ScrapeBogos:
    def __init__(self, url, keywords, keywordMultiWord, prefixText, postfixText):
        self.url = url
        self.keywords = keywords
        self.keywordMultiWord = keywordMultiWord
        self.prefixText = prefixText
        self.postfixText = postfixText
        self.itemsFound = []

    def initialize(self):
        response = requests.get(self.url, timeout=5)
        content = BeautifulSoup(response.content, "html.parser")
        # print(content)
        self.__parseItems(content)

    def getItemsFound(self):
        return self.itemsFound

    def __parseItems(self, content):
        bogoItems = content.findAll("div", attrs={"class": "theTileContainer"})
        beerItems = []
        # Get bogo item name
        for bogoItem in bogoItems:
            itemName = (
                bogoItem.find("div", attrs={"class": "title"})
                .find("h2", attrs={"class": "ellipsis_text"})
                .text
            )
            # print(itemName)
            itemDealDiv = bogoItem.find("div", attrs={"class": "deal"})
            if itemDealDiv is None:
                continue
            itemSaleText = itemDealDiv.find(
                "span", attrs={"class": "ellipsis_text"}
            ).text
            # print(itemSaleText)

            saleText = None
            if self.__isBogo(itemSaleText):
                saleText = "BOGO"
            elif self.__isB2go(itemSaleText):
                saleText = "B2G1"

            if saleText is not None and self.__isKeywordMatch(itemName):
                itemDate = (
                    bogoItem.find("div", attrs={"class": "validDates"})
                    .find("span")
                    .text
                )
                itemDate = itemDate.strip().replace("\r\n", " ")
                combinedString = (
                    self.prefixText
                    + " "
                    + saleText
                    + ": "
                    + itemName
                    + " "
                    + self.postfixText
                    + " "
                    + itemDate
                )
                self.itemsFound.append(combinedString)

    def __isKeywordMatch(self, name):
        lowerName = name.lower()
        if self.keywordMultiWord:
            for s in self.keywords:
                if s in lowerName:
                    return True
        else:
            for s in lowerName.split(" "):
                if s in self.keywords:
                    return True

        return False

    def __isBogo(self, saleText):
        lowerText = saleText.lower()
        # Text for stating an item is BOGO is not the same every week
        bogoText = [
            "buy 1 get 1 free",
            "buy one get one free",
            "buy one get 1 free",
            "buy 1 get one free",
        ]
        return any(s in lowerText for s in bogoText)

    def __isB2go(self, saleText):
        lowerText = saleText.lower()
        # Text for stating an item is B2G1 is not the same every week
        b2goText = [
            "buy 2 get 1 free",
            "buy two get one free",
            "buy 2 get one free",
            "buy two get 1 free",
        ]
        return any(s in lowerText for s in b2goText)
