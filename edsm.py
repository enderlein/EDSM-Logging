import requests
import json

import config

def query(url, params):
    try:
        headers = {'User-Agent' : config.USER_AGENT}
        r = requests.get(url, params = params, headers = headers)
    
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    if r.text == '{}':
        raise Exception(f"Received empty object from query: url={url}, params={params}")

    else: 
        return json.loads(r.text)

# TODO: doc comments for classes System and Systems
class System():
    url_base = "https://www.edsm.net/api-system-v1/"

    #TODO: Factions endpoint

    @classmethod
    def traffic(self, systemName):
        """
        systemName* (string) - name of system 

        returns (dict)

        Queries EDSM to get traffic data for a single system
        """
        endpoint = "traffic"
        params = {'systemName' : systemName}
        
        return query(self.url_base + endpoint, params)

    @classmethod
    def stations(self, systemName):
        """
        systemName* (string) - name of system

        returns (dict)

        Queries EDSM to get information on stations in a given system
        """

        endpoint = "stations"
        params = {'systemName' : systemName}

        return query(self.url_base + endpoint, params)

    @classmethod
    def market(self, systemName, stationName):
        """
        systemName* (string) - name of system
        stationName* (string) - name of station in system

        returns (dict)

        Queries EDSM to get market information from a given station
        """
        
        endpoint = "stations/market"
        params = {'systemName' : systemName, 'stationName' : stationName}

        return query(self.url_base + endpoint, params)

    @classmethod
    def factions(self, systemName, showHistory = 0):
        """
        systemName* (string) - name of system
        showHistory (int) - show factions history (0 : False, 1 : True)

        returns (dict)

        Queries EDSM to get information on stations in a given system
        """

        endpoint = "factions"
        params = {'systemName' : systemName, 'showHistory' : showHistory}

        return query(self.url_base + endpoint, params)

class Systems():
    url_base = "https://www.edsm.net/api-v1/"

    @classmethod
    def sphere_systems(self, systemName, radius, showId = 0, 
        showCoordinates = 0, showPermit = 0, showInformation = 0, 
        showPrimaryStar = 0, includeHidden = 0, showAll = 0):
        """
        systemName* (string) - name of system at the center of the radius
        radius* (int) - radius of search sphere (in lightyears)

        showId (int) - (0 : False, 1 : True)
        showCoordinates (int) - (0 : False, 1 : True)
        showPermit (int) - (0 : False, 1 : True)
        showInformation (int) - (0 : False, 1 : True)
        showPrimaryStar (int) - (0 : False, 1 : True)
        includeHidden (int) - (0 : False, 1 : True)

        showAll (int) - 0 : False, 1 : True - whether to set all optional args to 1

        returns (dict)

        Queries EDSM to get information on systems within a sphere radius of given system
        """

        if showAll:
            showId = 1
            showCoordinates = 1
            showPermit = 1
            showInformation = 1
            showPrimaryStar = 1
            includeHidden = 1

        endpoint = "sphere-systems"
        params = {'systemName' : systemName, 
        'radius' : radius, 
        'showId' : showId,
        'showCoordinates' : showCoordinates,
        'showPermit' : showPermit,
        'showInformation' : showInformation,
        'showPrimaryStar' : showPrimaryStar,
        'includeHidden' : includeHidden}

        return query(self.url_base + endpoint, params)
