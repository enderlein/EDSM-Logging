import requests
import json
import aiohttp

async def traffic(system_name, cache = False):
    """
    system_name* (string) - name of system 
    cache (bool) - whether or not to use cached data (data in cache may be outdated)

    returns (dict)

    Queries EDSM to get traffic data for a single system
    """
    
    url = "https://www.edsm.net/api-system-v1/traffic"
    params = {'systemName' : system_name}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params = params) as r:
            return await r.json()


#@caching.cacheable
def systems_radius(system_name, radius, cache = False):
    """
    system_name* (string) - name of system at the center of the radius
    radius* (int) - radius of search sphere (in lightyears)
    cache (bool) - whether or not to use cached data (data in cache may be outdated)

    returns (dict)

    Queries EDSM to get information on systems within a sphere radius of given system
    """

    url = "https://www.edsm.net/api-v1/sphere-systems"
    params = {'systemName' : system_name, 'radius' : radius, 'showInformation' : 1}

    r = requests.get(url, params = params)
    d = json.loads(r.text)

    return d
