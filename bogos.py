from bs4 import BeautifulSoup
import requests

class ScrapeBogos:

  def __init__(self, url, pageParam, numPages):
    self.url = url
    self.pageParam = pageParam
    self.numPages = numPages
    self.beerList = []

  def initialize(self):
    print(self.url)
    response = requests.get(self.url, timeout=5)
    content = BeautifulSoup(response.content, "html.parser")
    # print(content)
    self.__parseItems(content)

  def getBeerList(self):
    return self.beerList

  def __parseItems(self, content):
    bogoItems = content.findAll('div', attrs={'class': 'theTileContainer'})
    beerItems = []
    # Get bogo item name
    for bogoItem in bogoItems:
      itemName = bogoItem.find('div', attrs={'class': 'title'}).find('h2', attrs={'class': 'ellipsis_text'}).text
      itemSaleText = bogoItem.find('div', attrs={'class': 'deal'}).find('span', attrs={'class': 'ellipsis_text'}).text
      # print(itemName)
      # print(itemSaleText)

      saleText = None
      if self.__isBogo(itemSaleText):
        saleText = 'BOGO'
      elif self.__isB2go(itemSaleText):
        saleText = 'B2G1'

      if saleText is not None and self.__isBeer(itemName):
        itemDate = bogoItem.find('div', attrs={'class': 'validDates'}).find('span').text
        itemDate = itemDate.strip().replace('\r\n', ' ')
        combinedString = '🍺 ' + saleText + ': ' + itemName + ' 🍺 ' + itemDate
        self.beerList.append(combinedString)

  def __isBeer(self, name):
    lowerName = name.lower()
    # Added space in the beginning to make sure it is a start of a new word
    beerText = [' beer', ' lager', ' ale', ' pilsner' , ' ipa']
    return any(s in lowerName for s in beerText)

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
