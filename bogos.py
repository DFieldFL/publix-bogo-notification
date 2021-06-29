from bs4 import BeautifulSoup
import requests

class ScrapeBogos:

  def __init__(self, url, keywords, prefixText, postfixText):
    self.url = url
    self.keywords = keywords
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
    bogoItems = content.findAll('div', attrs={'class': 'theTileContainer'})
    beerItems = []
    # Get bogo item name
    for bogoItem in bogoItems:
      itemName = bogoItem.find('div', attrs={'class': 'title'}).find('h2', attrs={'class': 'ellipsis_text'}).text
      # print(itemName)
      itemDealDiv = bogoItem.find('div', attrs={'class': 'deal'})
      if itemDealDiv is None:
        continue
      itemSaleText = itemDealDiv.find('span', attrs={'class': 'ellipsis_text'}).text
      # print(itemSaleText)

      saleText = None
      if self.__isBogo(itemSaleText):
        saleText = 'BOGO'
      elif self.__isB2go(itemSaleText):
        saleText = 'B2G1'

      if saleText is not None and self.__isKeywordMatch(itemName):
        itemDate = bogoItem.find('div', attrs={'class': 'validDates'}).find('span').text
        itemDate = itemDate.strip().replace('\r\n', ' ')
        combinedString = self.prefixText + ' ' + saleText + ': ' + itemName + ' ' + self.postfixText + ' ' + itemDate
        self.itemsFound.append(combinedString)

  def __isKeywordMatch(self, name):
    lowerName = name.lower()
    for s in lowerName.split(' '):
      if s in self.keywords:
        return True
    return False

  def __isBogo(self, saleText):
    lowerText = saleText.lower();
    # Text for stating an item is BOGO is not the same every week
    bogoText = ['buy 1 get 1 free', 'buy one get one free', 'buy one get 1 free', 'buy 1 get one free']
    return any(s in lowerText for s in bogoText)

  def __isB2go(self, saleText):
    lowerText = saleText.lower();
    # Text for stating an item is B2G1 is not the same every week
    b2goText = ['buy 2 get 1 free', 'buy two get one free', 'buy 2 get one free', 'buy two get 1 free']
    return any(s in lowerText for s in b2goText)
