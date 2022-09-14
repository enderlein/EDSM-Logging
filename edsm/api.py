import requests
import json
import edsm.config as config

def query(url, params):
    headers = {'User-Agent' : config.USER_AGENT}
    r = requests.get(url, params = params, headers = headers)
    r.raise_for_status()

    return json.loads(r.text)

class System():
    url_base = "https://www.edsm.net/api-system-v1/"

    @classmethod
    def traffic(self, systemName):
        """
        systemName* <string> - name of system 

        returns <dict>

        Queries EDSM to get traffic data for a single system
        """
        endpoint = "traffic"
        params = {'systemName' : systemName}
        return query(self.url_base + endpoint, params)

    @classmethod
    def stations(self, systemName):
        """
        systemName* <string> - name of system

        returns <dict>

        Queries EDSM to get information on stations in a given system
        """

        endpoint = "stations"
        params = {'systemName' : systemName}

        return query(self.url_base + endpoint, params)

    @classmethod
    def market(self, systemName, stationName):
        """
        systemName* <string> - name of system
        stationName* <string> - name of station in system

        returns <dict>

        Queries EDSM to get market information from a given station
        """
        
        endpoint = "stations/market"
        params = {'systemName' : systemName, 'stationName' : stationName}

        return query(self.url_base + endpoint, params)

    @classmethod
    def marketById(self, marketId):
        """
        marketId* <int> - in-game market Id

        returns <dict>

        Queries EDSM to get market information from a station with given marketId
        """

        endpoint = "stations/market"
        params = {'marketId' : marketId}

        return query(self.url_base + endpoint, params)

    @classmethod
    def factions(self, systemName, showHistory = 0):
        """
        systemName* <string> - name of system
        showHistory <bool> - show factions history

        returns <dict>

        Queries EDSM to get information on stations in a given system
        """

        endpoint = "factions"
        params = {'systemName' : systemName, 'showHistory' : int(showHistory)}

        return query(self.url_base + endpoint, params)

class Systems():
    url_base = "https://www.edsm.net/api-v1/"

    @classmethod
    def system(self, systemName:str, showId:bool = 0, 
        showCoordinates:bool = 0, showPermit:bool = 0, showInformation:bool = 0, 
        showPrimaryStar:bool = 0, includeHidden:bool = 0, showAllInfo:bool = 0):
        """
        arg: systemName* <string> - name of system

        arg: showId <bool>
        arg: showCoordinates <bool>
        arg: showPermit <bool>
        arg: showInformation <bool>
        arg: showPrimaryStar <bool>
        arg: includeHidden <bool>

        arg: showAllInfo <bool> - whether to set all optional args to True

        returns <dict>

        Queries EDSM to get information on a system
        """
        
        if showAllInfo:
            showId = 1
            showCoordinates = 1
            showPermit = 1
            showInformation = 1
            showPrimaryStar = 1
            includeHidden = 1

        endpoint = "system"
        params = {'systemName' : systemName, 
        'showId' : int(showId),
        'showCoordinates' : int(showCoordinates),
        'showPermit' : int(showPermit),
        'showInformation' : int(showInformation),
        'showPrimaryStar' : int(showPrimaryStar),
        'includeHidden' : int(includeHidden)}

        return query(self.url_base + endpoint, params)
        
    @classmethod
    def sphere_systems(self, systemName:str, radius:int, showId:bool = 0, 
        showCoordinates:bool = 0, showPermit:bool = 0, showInformation:bool = 0, 
        showPrimaryStar:bool = 0, includeHidden:bool = 0, showAllInfo:bool = 0):
        """
        arg: systemName* <string> - name of system at the center of the radius
        arg: radius* <int> - radius of search sphere (in lightyears)

        arg: showId <bool>
        arg: showCoordinates <bool>
        arg: showPermit <bool> 
        arg: showInformation <bool>
        arg: showPrimaryStar <bool>
        arg: includeHidden <bool>

        arg: showAllInfo <bool> - whether to set all optional args to True

        returns <dict>

        Queries EDSM to get information on systems within a sphere radius of given system
        """
        if showAllInfo:
            showId = 1
            showCoordinates = 1
            showPermit = 1
            showInformation = 1
            showPrimaryStar = 1
            includeHidden = 1

        endpoint = "sphere-systems"

        params = {'systemName' : systemName, 
        'radius' : radius, 
        'showId' : int(showId),
        'showCoordinates' : int(showCoordinates),
        'showPermit' : int(showPermit),
        'showInformation' : int(showInformation),
        'showPrimaryStar' : int(showPrimaryStar),
        'includeHidden' : int(includeHidden)}

        return query(self.url_base + endpoint, params)
