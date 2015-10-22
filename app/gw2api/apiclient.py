__author__ = 'Frenos'

import requests

from .endpoints import apiEndpoints, apiBaseUrl, apiLanguage


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

    def getItems(self, itemIds):
        # workaround fuer ids-parameter:
        # api braucht ids=1,2,3
        # request-param mit list erzeugt aber ids=1&ids=2...
        # daher liste in String und param als String
        # TODO: research more
        idsString = ",".join(str(x) for x in itemIds)
        return self.getItem(idsString=idsString)

    def getItem(self, itemId=None, idsString=None):
        url = apiBaseUrl + apiEndpoints["Items"]

        if idsString:
            ids = idsString
        elif itemId:
            ids = itemId

        params = {
                "lang": apiLanguage,
                "ids": ids
        }
        response = self.httpSession.get(url=url, params=params)
        return response.json()


    def getAllItems(self):
        allItemIds = self.getItemIds()

        # allItemIds hat Liste ueber alle Ids, api nimmt aber nur 200 api pro call
        # splitten in Liste mit 200er Chunks
        itemIdChunkList = []
        for i in range(0, len(allItemIds), 200):
            itemIdChunkList.append(allItemIds[i:i + 200])
        # itemIdChunkList hat etwa 250 Listen mit je 200 Items

        allItems = []
        for chunk in itemIdChunkList:
            allItems.extend(self.getItems(chunk))

        return allItems


    def getBankContent(self):
        url = apiBaseUrl+apiEndpoints["AccountBank"]
        params = {
            "lang" : apiLanguage,
            "access_token" : self.api_key
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
        currencyIds = response.json()
        idsString = ",".join(str(x) for x in currencyIds)
        params = {
            "lang": apiLanguage,
            "ids": idsString
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
