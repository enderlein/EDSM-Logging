import requests
import json
import caching

def traffic(system_name):
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
    # center_system_name - name of system at the center of radius search
    url = "https://www.edsm.net/api-v1/sphere-systems"
    params = {'systemName' : center_system_name, 'radius' : radius, 'showInformation' : 1}

    r = requests.get(url, params = params)
    d = json.loads(r.text)

    return d

def traffic_radius(center_system_name, radius, min_pop = -1):
    # center_system_name - name of system which will be center of sphere
    # radius - radius of the sphere
    # get traffic data from systems in a sphere radius

    systems = systems_radius(center_system_name, radius) 

    r = []
    for system in systems:
        if 'population' in system['information']:
            if system['information']['population'] > min_pop:
                d = {'name' : system['name'],
                        'traffic' : traffic(system['name'])['traffic']}
                r.append(d)
    
    return r

def traffic_report(dump_file_name, sys_name, radius, min_pop = -1):
    # dump neat(er) traffic data into a text file
    tr = traffic_radius(sys_name, radius, min_pop)
    with open(dump_file_name, 'a') as f:
        for report in tr:
            f.write(json.dumps(report) + '\n')

# traffic_report('data.txt', 'Alcor', 20, min_pop = 20000)