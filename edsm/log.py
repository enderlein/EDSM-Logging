import json
import time
import logging

from concurrent.futures import ThreadPoolExecutor, wait, Future

from logging import INFO, DEBUG
from typing import Callable

import edsm.models as models
import edsm.api as api
import edsm.config as config


"""
For storing timstamped system data.

Designed around collecting data to help spot trends in market and traffic data 
based on the powerplay cycle (regular edsm.net traffic data only goes back one week, market data only one day) 
"""

# TODO: Scheduling
# TODO: Import config with from calls (not that big a module, but less overhead anyways)
# TODO: Finish annotating

# TODO: ABCs lol
# 

logging.basicConfig(level=INFO)

def submit_updates(executor:ThreadPoolExecutor, tasks:list[Callable[[None], None]]):
    futures = []
    for task in tasks:
        future = executor.submit(task)
        futures.append(future)

    return futures

def check_futures(futures:list[Future]):
    wait(futures)
    
    for future in futures:
        if future.exception():
            raise future.exception()


class SystemsLogger():
    """
    __init__
        arg keys* <list> - keys to grab from <System> objects in self._systems when logging
        arg delay <int> - amount of time to wait after collecting data. Defaults to config.DEFAULT_SLEEP

    property systems <list> - list of systems being managed by <Self>

    method parse_key(obj, key) <Any> - grabs given keys from given object
        arg obj* <models.System>
        arg key* <str or int>

    method gather_keys <list>
    method update_by_keys <None>
    """

    
    def __init__(self, keys:dict[str, list[str]], delay:int=config.DEFAULT_SLEEP):
        self.keys = keys
        self.delay = delay

        self._systems = None

        # to be overwritten by children (TODO: ABCs lol)
        self.filename = f'{self}.json'
        self.systems_data = None # TODO: clunky and weird to have seperate sphere class, 
                                    # make systems_data var an init arg, and just init it with api.Systems.sphere_systems()

        self.update_keybinds = {
            'traffic' : [self.update_traffic],
            'stations' :  [self.update_stations, self.update_stations_markets]
        }

        # TODO: add check_keys method to make sure provided keys are expected format
        # NOTE: no data is saved if an exception is thrown in the middle of running updates (self.update_by_keys)
        # so it is very important that provided keys are clean and parseable BEFORE running updates. 

    
    @property
    def systems(self) -> list[models.System]:
        if not self._systems:
            self._systems = [models.System(d) for d in self.systems_data]

        return self._systems

    # TODO: rename? 'filter' is more accurate than 'gather'
    def gather_by_keys(self) -> list[dict]:
        logging.info("Gathering data by keys")
        # creates a list of dicts containing system data indicated by self.keys

        l = []
        for system in self.systems:
            system_data = {}
            #TODO: there has got to be a better way. more binding dicts?

            for key in self.keys.keys():
                if key == 'system':
                    system_data['system'] = system.get_keys(self.keys.get('system'))
                if key == 'traffic':
                    system_data['traffic'] = system.traffic.get_keys(self.keys.get('traffic')) 
                if key == 'stations':
                    system_data['stations'] = system.stations.get_keys(self.keys.get('stations'))

            l.append(system_data)

        return l

    def update_by_keys(self):
        logging.info("Running updates")
        # update depending on which keys are provided
        if not any([key in self.update_keybinds.keys() for key in self.keys]):
            logging.info("No updates to run")
            
        else:
            for key in self.keys.keys():
                # NOTE: using .get() to avoid raising errors
                binding_list = self.update_keybinds.get(key)

                if binding_list:
                    for update_routine in binding_list:
                        update_routine()

    def update_traffic(self):
        """Update all <Traffic> objects using :config.MAX_THREADS: workers"""
        logging.info("Updating traffic") # TODO: create list-like container class for <System> objs, move threading logic there 
        
        with ThreadPoolExecutor(max_workers = config.MAX_THREADS) as executor:
            futures = submit_updates(executor, [system.traffic.update for system in self.systems])
            check_futures(futures)

    def update_stations(self):
        """Update all <Stations> objs (attr of <Systems> objs in self.systems) using :config.MAX_THREADS: workers"""
        logging.info("Updating stations (may take a while)")     

        with ThreadPoolExecutor(max_workers = config.MAX_THREADS) as executor:
            futures = submit_updates(executor, [system.stations.update for system in self.systems])
            check_futures(futures)

    def update_stations_markets(self):
        """Update data for all <Market> objs (attr of <Stations> objs) using :config.MAX_THREADS: workers"""
        logging.info("Updating station markets (may take a while)")

        with ThreadPoolExecutor(max_workers=config.MAX_THREADS) as executor:
            tasks = []
            for system in self.systems:
                for station in system.stations.stations:
                    tasks.append(station.update_market)

            futures = submit_updates(executor, tasks)
            check_futures(futures)

    def get_payload(self) -> list[dict]:
        """ Return list containing dicts containing payload (timstamp + systems data)"""

        # Returned in this format for the sake of convienience when calling self.append_json()
        logging.info("Building payload")

        timestamp = int(time.time())
        system_data = self.gather_by_keys()

        # TODO: Model as class?
        return [{'timestamp' : timestamp, 'systems' : system_data}]

    
    #TODO: Change something here to specify that this func only appends arrays (maybe rename to append_json_array())
    def append_json(self, file:str, data:list[dict]):
        # expecting data from file to be parseable as json array
        # default old_data to empty list if given file doesn't exist or has invalid json (really only want to check for empty files, 
        # should stop/throw warning if there is data but its not valid json. TODO: narrow second exception)
        logging.info(f"Writing payload to file: \'{self.filename}\'")
        try:
            file_read = open(file, 'r')
            old_data = json.loads(file_read.read())
            file_read.close()
                
        except (FileNotFoundError, json.decoder.JSONDecodeError): # as e:
            # TODO: log exception (as warning)
            old_data = []

        merged_data = json.dumps(old_data + data, indent=config.JSON_INDENT)

        file_write = open(file, 'w')
        file_write.write(merged_data)

        file_write.close()

    def log(self):
        logging.info("Starting log routine...")
        # TODO: change function name, 'log' might be confusing
        # Timestamps and dumps captured data as json to file :<self>.filename:
        self.update_by_keys()
        
        payload = self.get_payload()
        self.append_json(self.filename, payload)
    
    def sleep(self):
        sleep_time = time.strftime("%H:%M:%S", time.localtime())
        logging.info(f"{self} :SLEEPING: for {self.delay} seconds (since {sleep_time})")

        time.sleep(self.delay)

    def run(self):
        while True:
            self.log()
            self.sleep()
        

class SphereLogger(SystemsLogger):
    def __init__(self, center, radius, keys, delay=config.DEFAULT_SLEEP):
        super().__init__(keys, delay=delay)

        self.filename = f"{center} - {radius}ly.json" 
        self.systems_data = api.Systems.sphere_systems(center, radius, showAllInfo=1) # NOTE TODO: showAllInfo clunky and wasteful, 
                                                                                        # should toggle flags based on keys

        # TODO: method for updating systems data!
"""
class SphereLogger():
    def __init__(self, sphere: traffic.TrafficSphere, sleep):
        self.sleep = sleep
        self.traffic_sphere = sphere
    
    def append_file(self, file, data):
        with open(file, 'a') as f:
            f.write(data + '\n')

    def run(self):
        while True:
            self.traffic_sphere.update_all()
            filename = f"traffic_sphere_centered@{self.traffic_sphere.center}"
            for traffic_monitor in self.traffic_sphere.monitors:
                s = json.dumps(traffic_monitor.traffic)
                
                
                self.append_file(filename, s)

            current_time = time.strftime("%H:%M:%S", time.localtime())
            print(f"{self} :Sleeping: for {self.sleep} seconds (since {current_time})")
            time.sleep(self.sleep)


def get_loggers(*names, radius, sleep):
    spheres = [traffic.TrafficSphere(name, radius) for name in names]
    loggers = [SphereLogger(sphere, sleep) for sphere in spheres]

    return loggers

def main():
    loggers = get_loggers('Warkawa', 'Sol', radius = 8, sleep = 20)

    with ThreadPoolExecutor(max_workers=2) as executor:
        for l in loggers:
            executor.submit(l.run)

if __name__ == "__main__":
    main()
"""
