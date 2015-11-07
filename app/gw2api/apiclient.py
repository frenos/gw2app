__author__ = 'Frenos'

import requests

from .endpoints import apiEndpoints, apiBaseUrl, apiLanguage
from helpers import idList2String, idList2Chunks


class ApiClient:
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
        url = apiBaseUrl + apiEndpoints["Characters"]
        params = {"access_token": self.api_key,
                  "ids": character,
                  "lang": apiLanguage}
        response = self.httpSession.get(url=url, params=params)
        # TODO:Fehlercheck
        return response.json()

    def getItemIds(self):
        """ gets all available item-ids
                returns them in a list
        """
        url = apiBaseUrl + apiEndpoints["Items"]
        params = {"lang": apiLanguage}
        response = self.httpSession.get(url=url, params=params)
        return response.json()

    def getItemIdsChunked(self):
        allItemIds = self.getItemIds()
        return idList2Chunks(allItemIds)

    def getItem(self, itemId=None, idsString=None):
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
        itemIdChunkList = self.getItemIdsChunked()
        allItems = []
        for chunk in itemIdChunkList:
            allItems.extend(self.getItem(idsString=chunk))
        return allItems

    def getBankContent(self):
        url = apiBaseUrl + apiEndpoints["AccountBank"]
        params = {
            "lang": apiLanguage,
            "access_token": self.api_key
        }
        response = self.httpSession.get(url=url, params=params)

        bankContents = response.json()
        return bankContents

    def getCurrencies(self):
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
        """ gets all available price-ids
                returns them in a list
        """
        url = apiBaseUrl + apiEndpoints["ItemPrices"]
        params = {"lang": apiLanguage}
        response = self.httpSession.get(url=url, params=params)
        return response.json()

    def getPriceIdsChunked(self):
        allPriceIds = self.getPriceIds()
        return idList2Chunks(allPriceIds)

    def getPrice(self, itemId=None, idsString=None):
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
        url = apiBaseUrl + apiEndpoints["AccountWallet"]
        params = {
            "lang": apiLanguage,
            "access_token": self.api_key
        }
        response = self.httpSession.get(url=url, params=params)
        return response.json()
