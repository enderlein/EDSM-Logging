import requests
import json

def traffic(system_name):
    """
    system_name* (string) - name of system 
    cache (bool) - whether or not to use cached data (data in cache may be outdated)

    returns (dict)

    Queries EDSM to get traffic data for a single system
    """
    
    url = "https://www.edsm.net/api-system-v1/traffic"
    params = {'systemName' : system_name}
    
    try:
        r = requests.get(url, params = params)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    d = json.loads(r.text)

    if d:
        return d

    elif d == {}: 
        raise Exception(f"Received empty object in edsm.traffic('{system_name}')")



def systems_radius(system_name, radius):
    """
    system_name* (string) - name of system at the center of the radius
    radius* (int) - radius of search sphere (in lightyears)
    cache (bool) - whether or not to use cached data (data in cache may be outdated)

    returns (dict)

    Queries EDSM to get information on systems within a sphere radius of given system
    """

    url = "https://www.edsm.net/api-v1/sphere-systems"
    params = {'systemName' : system_name, 'radius' : radius, 'showInformation' : 1}

    try:
        r = requests.get(url, params = params)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    d = json.loads(r.text)

    if d:
        return d

    elif d == {}: 
        raise Exception(f"Received empty object in edsm.traffic('{system_name}', {radius})")
