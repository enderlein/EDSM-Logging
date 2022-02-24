import requests
import json

import caching

# TODO: results should be written to cache for potential use later, regardless cached = True/False
def traffic(system_name, cached = False):
    """
    system_name* (string) - name of system 
    cached (bool) - whether or not to use cached data (data in cache may be outdated)

    returns (dict)

    Queries EDSM to get traffic data for a single system
    """
    
    # check if system traffic data is in cache already
    url = "https://www.edsm.net/api-system-v1/traffic"
    params = {'systemName' : system_name}
    
    # TODO: just turn this into a decorator
    if not cached:
        r = requests.get(url, params = params)
        d = json.loads(r.text)

        return d

    elif cached:
        c = caching.Cache('traffic')

        # search cache, return search result if found
        cache_search = c.search(url, params)
        if cache_search:
            return cache_search

        else:
            # get from api and add to cache if not found in cache
            r = requests.get(url, params = params)
            d = json.loads(r.text)

            c.write(url, params, d)

        return d

def systems_radius(system_name, radius, cached = False):
    """
    system_name* (string) - name of system at the center of the radius
    radius* (int) - radius of search sphere (in lightyears)
    cached (bool) - whether or not to use cached data (data in cache may be outdated)

    returns (dict)

    Queries EDSM to get information on systems within a sphere radius of given system
    """

    url = "https://www.edsm.net/api-v1/sphere-systems"
    params = {'systemName' : system_name, 'radius' : radius, 'showInformation' : 1}

    if not cached:
        r = requests.get(url, params = params)
        d = json.loads(r.text)

        return d

    elif cached:
        c = caching.Cache('systems_radius')

        # search cache, return search result if found
        cache_search = c.search(url, params)
        if cache_search:
            return cache_search

        else:
            # get from api and add to cache if not found in cache
            r = requests.get(url, params = params)
            d = json.loads(r.text)

            c.write(url, params, d)

        return d