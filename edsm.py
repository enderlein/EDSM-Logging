import requests
import json

import caching

def traffic(system_name):
    # STRING - system_name - name of syetem to get traffic data from
    #
    # returns DICT
    #
    # Queries EDSM to get traffic data from given system
    #############################
    
    # check if system traffic data is in cache already
    c = caching.Cache('traffic')

    url = "https://www.edsm.net/api-system-v1/traffic"
    params = {'systemName' : system_name}

    cache_search = c.search(url, params)
    if cache_search:
        return cache_search

    # if not in cache get from api and add to cache
    else:
        r = requests.get(url, params = params)
        d = json.loads(r.text)

        # add to cache
        c.write(url, params, d)

        return d

def systems_radius(center_system_name, radius):
    # STRING - center_system_name - name of system at the center of radius search
    # INT ---- radius - radius of sphere
    #
    # returns DICT
    #
    # Queries EDSM to get information on systems within a sphere radius from
    # given system.
    #############################################
    c = caching.Cache('systems_radius')

    url = "https://www.edsm.net/api-v1/sphere-systems"
    params = {'systemName' : center_system_name, 'radius' : radius, 'showInformation' : 1}

    cache_search = c.search(url, params)
    if cache_search:
        return cache_search

    else:
        r = requests.get(url, params = params)
        d = json.loads(r.text)

        c.write(url, params, d)

        return d