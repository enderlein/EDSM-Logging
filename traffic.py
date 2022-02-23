import json
import time

import edsm

def traffic_radius(center_system_name, radius, min_pop = -1):
    # STRING - center_system_name - name of system which will be center of sphere
    # INT ---- radius - radius of the sphere
    # INT ---- min_pop - minimum population; func will not query api for traffic data from systems
    #                    with a population below this value
    #
    # returns DICT
    #
    # Get traffic data from systems in a sphere radius
    ###############################
    systems = edsm.systems_radius(center_system_name, radius) 

    r = {}
    for system in systems:
        if 'population' in system['information']:
            if system['information']['population'] > min_pop:
                d = {'traffic' : edsm.traffic(system['name'])['traffic']}
                r[system['name']] = d
    
    return r

def traffic_report(sys_name, radius, min_pop = -1, filename = None, dumps = False):
    # dump neat(er) traffic data into a text file

    if not filename:
        default = f'{sys_name}-{int(time.time())}.json'
        filename = default
    tr = traffic_radius(sys_name, radius, min_pop)
    
    if dumps:
        with open(filename, 'a') as f:
            f.write(json.dumps(tr) + '\n')

    return tr



