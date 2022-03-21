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

    #TODO: Market endpoint, Factions endpoint

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

#TODO: write tests
#
class Systems():
    url_base = "https://www.edsm.net/api-v1/"

    @classmethod
    def sphere_systems(self, systemName, radius, showId = 0, 
        showCoordinates = 0, showPermit = 0, showInformation = 0, 
        showPrimaryStar = 0, includeHidden = 0):
        """
        systemName* (string) - name of system at the center of the radius
        radius* (int) - radius of search sphere (in lightyears)

        returns (dict)

        Queries EDSM to get information on systems within a sphere radius of given system
        """

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
