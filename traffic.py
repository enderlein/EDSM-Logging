import json
import time

import edsm
# build class TrafficMonitor, use Traffic model to build Traffic monotiring network 
# TODO: TrafficSphere
# TODO: Update on a schedule
# TODO: Cross-reference hour-by-hour traffic data to track players.

"""
 MODEL ShipRoute
    Models ships suspected routes

    attribute route:
        returns dict containing route info

    method add(system):
        add system to route

    method remove(system):
        remove system from route

 MODEL TrafficMonitor
    Performs higher-level functions for the TrafficSpheres

    attribute update_queue:
        array of traffic objects in traffic queue

    attribute routes:
        returns array of possible routes

    method create_sphere(name)
        Creates TrafficSphere at system, adds to update queue
        name - name of center system

    method remove_sphere(name)
        Removes sphere that has given system name as center from the update queue
        name - name of center system

    method run()
        Add current center point to update_queue
        Run updates until a traffic object detects a change in traffic data AND breakdown data (need ship name as an identifier)
        Add entire sphere to update queue
        Run updates until at least one traffic object detects a change 
        Check if change in breakdown data corresponds to initlal change in breakdown data
        If so, 
            Log the ship name and its route using a Route model
            Remove current sphere from update queue
            Center current sphere at that system

        

    method track()

"""

"""
MODEL TrafficSphere
    Array of Traffic objects, set up as a sphere around a center system.

    attribute center = traffic object at center of sphere

    method get_radius(radius, name)
        Gets Traffic objects within given radius of a system within sphere
        name - name of system
        radius - radius to search in (max distance)


"""

# TODO: add 'diff' method that detects changes in traffic data from last update

class TrafficMonitor():
    def __init__(self, name):
        self.name = name
        self._traffic = None
    
    @property
    def traffic(self):
        if not self._traffic:
            t = edsm.traffic(self.name)
            d = {'traffic' : t['traffic'],
                'breakdown' : t['breakdown'],
                'timestamp' : int(time.time())}

            self._traffic = d

        return self._traffic

    def update(self):
        t = edsm.traffic(self.name)
        d = {'traffic' : t['traffic'],
            'breakdown' : t['breakdown'],
            'timestamp' : int(time.time())}

        self._traffic = d



# TODO: Add loading bar or something
def traffic_radius(*, system_name, radius, min_pop = -1, filename = None, dumps = False, cache = False):
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
    
    systems = edsm.systems_radius(system_name = system_name, radius = radius, cache = cache)

    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))

    r = {'timestamp' : timestamp, 'data' : {}}

    for system in systems:
        if 'population' in system['information']:
            if system['information']['population'] > min_pop:
                t = edsm.traffic(system_name = system['name'], cache = cache)
                d = {'traffic' : t['traffic'],
                    'breakdown' : t['breakdown']} ### NOTE format
                r['data'][system['name']] = d
    
    if dumps:
        if not filename:
            default = f'{system_name}-{int(time.time())}.json'
            filename = default

        with open(filename, 'a') as f:
            f.write(json.dumps(r) + '\n')

    return r


