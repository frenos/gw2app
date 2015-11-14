__author__ = 'Frenos'

from ..gw2api.apiclient import ApiClient
from ..database import db
from ..database.models import Map


class CommonDb:
    def __init__(self, api_key):
        self.apiClient = ApiClient(api_key)

    def updateMaps(self):
        """
        Will update the available maps
        @return: no return value
        """
        mapData = self.apiClient.getMaps()
        if len(mapData) > 0:
            for map in mapData:
                mapObj = Map.query.get(map['id'])
                if not mapObj:
                    newMap = Map(id=map['id'],
                                 name=map['name'],
                                 min_level=map['min_level'],
                                 max_level=map['max_level'],
                                 region_id=map['region_id'],
                                 region_name=map['region_name'],
                                 continent_id=map['continent_id'],
                                 continent_name=map['continent_name'])
                    db.session.add(newMap)
            db.session.commit()
