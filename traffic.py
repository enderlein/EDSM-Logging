import json
import time

import edsm

# TODO: Add loading bar or something
def traffic_radius(*, system_name, radius, min_pop = -1, filename = None, dumps = False, use_cache = False):
    """
    system_name* (string) - name of system at center of search sphere.
    radius* (int) - radius of search sphere (in lightyears).
    min_pop (int) - minimum population, will not query api for traffic data from systems with a population below this value.
    filename (string) - name of file to dump to (if dumps = True).
    dumps (bool) - whether or not data is dumped to file (formatted as json).
    use_cache (bool) - whether or not to use cached data (data in cache may be outdated)
     
    returns (dict)
    
    Get traffic data from systems in a sphere
    """
    
    systems = edsm.systems_radius(system_name, radius, cached = use_cache)

    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))

    r = {'timestamp' : timestamp, 'data' : {}}

    for system in systems:
        if 'population' in system['information']:
            if system['information']['population'] > min_pop:
                d = {'traffic' : edsm.traffic(system['name'], cached = use_cache)['traffic']}
                r['data'][system['name']] = d
    
    if dumps:
        if not filename:
            default = f'{system_name}-{int(time.time())}.json'
            filename = default

        with open(filename, 'a') as f:
            f.write(json.dumps(r) + '\n')

    return r



