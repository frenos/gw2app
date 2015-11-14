__author__ = 'Frenos'

import requests

from helpers import idList2String, idList2Chunks
from .endpoints import apiEndpoints, apiBaseUrl, apiLanguage


class ApiClient:
    """
    Class to connect to Gw2-Api, needs an API-KEY to work.
    """
    def __init__(self, apikey):
        self.api_key = apikey
        self.httpSession = requests.Session()

    def getCharacters(self):
        """Gets all character-names of the account.
        Needs a valid apikey set for the instance.
        returns character-names as list or empty list if no api_key set.
        """
        if (self.api_key):
            # do sth
            url = apiBaseUrl + apiEndpoints["Characters"]
            params = {"access_token": self.api_key}
            response = self.httpSession.get(url=url, params=params)
            # TODO:Fehlercheck
            return response.json()
        else:
            # TODO: logging error
            return []

    def GetCharacterInformation(self, character):
        """
        Gets information about a character.
        :param character: character to get information about
        :return: information as dict
        """
        url = apiBaseUrl + apiEndpoints["Characters"]
        params = {"access_token": self.api_key,
                  "ids": character,
                  "lang": apiLanguage}
        response = self.httpSession.get(url=url, params=params)
        # TODO:Fehlercheck
        return response.json()

    def getMaps(self):
        """
        Get information about maps from the api.
        :return: information about all maps as list of dict
        """
        url = apiBaseUrl + apiEndpoints["Maps"]
        params = {"lang": apiLanguage}
        response = self.httpSession.get(url=url, params=params)
        mapIds = response.json()
        mapData = []
        if len(mapIds) > 0:
            mapdIsChunked = idList2Chunks(mapIds)
            for chunk in mapdIsChunked:
                idsString = idList2String(chunk)
                params = {"lang": apiLanguage,
                          "ids": idsString}
                response = self.httpSession.get(url=url, params=params)
                mapData.extend(response.json())
        return mapData

    def getItemIds(self):
        """
        Get all available itemId from API.
        :return: list of all itemId available
        """
        url = apiBaseUrl + apiEndpoints["Items"]
        params = {"lang": apiLanguage}
        response = self.httpSession.get(url=url, params=params)
        return response.json()

    def getItemIdsChunked(self):
        """
        Get all available itemId from API and return them chunked.
        :return: list of lists of itemIds
        """
        allItemIds = self.getItemIds()
        return idList2Chunks(allItemIds)

    def getItem(self, itemId=None, idsString=None):
        """
        Get Details about an item or multiple items
        :param itemId: Set if only item
        :param idsString: Set to get multiple Items at once
        :return: (list of) dict of details about items
        """
        url = apiBaseUrl + apiEndpoints["Items"]

        if idsString:
            ids = idList2String(idsString)
        elif itemId:
            ids = itemId

        params = {
            "lang": apiLanguage,
            "ids": ids
        }
        response = self.httpSession.get(url=url, params=params)
        return response.json()

    def getAllItems(self):
        """
        Get all itemDetails in one big list.
        :return: list of all available item-details.
        """
        itemIdChunkList = self.getItemIdsChunked()
        allItems = []
        for chunk in itemIdChunkList:
            allItems.extend(self.getItem(idsString=chunk))
        return allItems

    def getBankContent(self):
        """
        Get the current contents of the bank.
        :return: list of dict about bank contents
        """
        url = apiBaseUrl + apiEndpoints["AccountBank"]
        params = {
            "lang": apiLanguage,
            "access_token": self.api_key
        }
        response = self.httpSession.get(url=url, params=params)

        bankContents = response.json()
        return bankContents

    def getCurrencies(self):
        """
        Get all currencies known to the game.
        :return: a list of dict with information about currencies
        """
        url = apiBaseUrl + apiEndpoints["Currencies"]
        params = {
            "lang": apiLanguage
        }
        response = self.httpSession.get(url=url, params=params)
        # feed response-list in helper to format it into a string ids=1,2,3
        idsString = idList2String(response.json())
        params = {
            "lang": apiLanguage,
            "ids": idsString
        }
        response = self.httpSession.get(url=url, params=params)
        return response.json()

    def getPriceIds(self):
        """
        Get all available price-ids.
        :return: list of ids
        """
        url = apiBaseUrl + apiEndpoints["ItemPrices"]
        params = {"lang": apiLanguage}
        response = self.httpSession.get(url=url, params=params)
        return response.json()

    def getPriceIdsChunked(self):
        """
        Get all available price-ids.
        :return: list of list of price-ids
        """
        allPriceIds = self.getPriceIds()
        return idList2Chunks(allPriceIds)

    def getPrice(self, itemId=None, idsString=None):
        """
        Get price-information either about a single item or a list of items.
        :param itemId: set to get information about one item
        :param idsString: set to get information about multiple items at once
        :return: (list of) dict with information
        """
        url = apiBaseUrl + apiEndpoints["ItemPrices"]

        if idsString:
            ids = idList2String(idsString)
        elif itemId:
            ids = itemId

        params = {
            "lang": apiLanguage,
            "ids": ids
        }
        response = self.httpSession.get(url=url, params=params)
        return response.json()

    def getWalletContent(self):
        """
        Get current status of currencies the account collected.
        :return: list of dict with currency-values
        """
        url = apiBaseUrl + apiEndpoints["AccountWallet"]
        params = {
            "lang": apiLanguage,
            "access_token": self.api_key
        }
        response = self.httpSession.get(url=url, params=params)
        return response.json()

    def getPvPMatchIds(self):
        """
        Get ids of last 10 played matches.
        :return: list of match-ids
        """
        url = apiBaseUrl + apiEndpoints["PvpMatches"]
        params = {
            "lang": apiLanguage,
            "access_token": self.api_key
        }
        response = self.httpSession.get(url=url, params=params)
        return response.json()

    def getPvPMatchDetails(self):
        """
        Get information about last 10 played pvp-matches.
        :return: list of dict with match-information
        """
        idsString = idList2String(self.getPvPMatchIds())
        url = apiBaseUrl + apiEndpoints["PvpMatches"]
        params = {
            "lang": apiLanguage,
            "access_token": self.api_key,
            "ids": idsString
        }
        response = self.httpSession.get(url=url, params=params)
        return response.json()

    def getTransactionsHistory(self, sells=None, buys=None):
        """
        Get Tradingpost-transactions of the account.
        :param sells: set to True to get Sell transaction
        :param buys: set to True to get Sell transaction
        :return: list of dict with information about transactions
        """
        url = apiBaseUrl + apiEndpoints["AccountTransactions"] + "/history"
        if sells:
            url = url + "/sells"
        elif buys:
            url = url + "/buys"
        page = 0
        page_size = 200
        params = {
            "lang": apiLanguage,
            "access_token": self.api_key,
            "page": page,
            "page_size": page_size
        }
        myTransactions = []
        response = self.httpSession.get(url=url, params=params)
        Transactions = response.json()
        myTransactions.extend(Transactions)
        if 'next' in response.links:
            while True:
                page = page + 1
                params["page"] = page
                print("getting page " + str(page))
                response = self.httpSession.get(url=url, params=params)
                Transactions = response.json()
                myTransactions.extend(Transactions)
                if not 'next' in response.links:
                    break
        return myTransactions
