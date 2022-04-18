import json
import time

from concurrent.futures import ThreadPoolExecutor
from typing import Any, Union

import edsm.models as models
import edsm.api as api
import edsm.config as config

# TODO: Import config with from calls (not that big a module, but less overhead anyways)
# TODO: logging
# TODO: Annotate
# TODO: As of now, resulting .json files are kinda large, esp. if i wanna be using this to store years-worths of data
# find ways to save on space, remove extranneous data, modify indent maybe?
# TODO: ABCs lol
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
    def __init__(self, keys:list, delay:int=config.DEFAULT_SLEEP):
        self.keys = keys
        self.delay = delay

        self._systems = None

        # to be overwritten by children (TODO: ABCs lol)
        self.filename = f'{self}.json'
        self.systems_data = None

    @property
    def systems(self) -> list[models.System]:
        if not self._systems:
            # list[models.System(d) for d in self.systems_data]
            self._systems = list(map(lambda d: models.System(d), self.systems_data))

        return self._systems

    def parse_key(self, obj:models.System, key:Union[str, int]) -> Any:
        # method for grabbing data from <models.System> objects 
        # TODO: Add support for grabbing individual stations with keys formatted like "stations[Ray Hub]"

        if isinstance(obj.__dict__[key], models.Traffic):
            return obj.__dict__[key].dumpdict()

        # TODO: SHOULD WORK, BUT JUST A TEMPLATE
        if isinstance(obj.__dict__[key], models.Stations):
            return obj.__dict__[key].dumpdict()

        return obj.__dict__[key]

    def gather_keys(self) -> list:
        print("Gathering data by keys")
        # creates a list of dicts containing system data indicated by self.keys

        # list[dict{k : self.parse_key(system, k) for k in self.keys} for system in self.systems]
        return list(map(lambda system: dict(map(lambda k: (k, self.parse_key(system, k)), self.keys)), self.systems))

    def update_by_keys(self):
        print("Updating data by keys")
        # update depending on which keys are needed
        # TODO: Find a better way to toggle these, maybe a dict with keys tied to update calls
        if 'traffic' in self.keys:
            self.update_traffic()

        if 'stations' in self.keys:
            self.update_stations()
            
            self.update_stations_markets()

    def update_traffic(self):
        print("Updating traffic")
        # Update all traffic objects using :config.MAX_THREADS: workers
        with ThreadPoolExecutor(max_workers = config.MAX_THREADS) as executor:
            for system in self.systems:
                executor.submit(system.traffic.update)

    def update_stations(self):
        print("Updating stations")
        # Update all stations objects using :config.MAX_THREADS: workers
        with ThreadPoolExecutor(max_workers = config.MAX_THREADS) as executor:
            for system in self.systems:
                executor.submit(system.stations.update)

    def update_stations_markets(self):
        print("Updating station markets")
        with ThreadPoolExecutor(max_workers=config.MAX_THREADS) as executor:
            for system in self.systems:
                for station in system.stations.stations:
                    executor.submit(station.update_market)
        
    def append_json(self, file, data):
        # expecting data from file to be parseable as json array
        # default old_data to empty list if given file doesn't exist or has invalid json (really only want to check for empty files, 
        # should stop or throw warning if there is data but its not valid json. TODO: narrow second exception)
        try:
            file_read = open(file, 'r')
            old_data = json.loads(file_read.read())
            file_read.close()
                
        except (FileNotFoundError, json.decoder.JSONDecodeError): # as e:
            # TODO: log exception (as warning)
            old_data = []

        merged_data = json.dumps(old_data + data)

        file_write = open(file, 'w')
        file_write.write(merged_data)

        file_write.close()

    def log(self):
        print("Starting to gather. . .")
        # Timestamps and dumps captured data as json to file :<self>.filename:
        #TODO: reorganize above methods so that it's easier to follow program flow
        self.update_by_keys()
        timestamp = int(time.time())

        # TODO: Generalize as generate_json() method
        # so it's easier to implement switching to other output formats (i.e csv, idk)
        payload = self.gather_keys()
        #TODO: map
        for system in payload:
            system['timestamp'] = timestamp
        
        self.append_json(self.filename, payload)
    
    def sleep(self):
        # TODO: Replace print with logging event
        sleep_time = time.strftime("%H:%M:%S", time.localtime())
        print(f"{self} :Sleeping: for {self.delay} seconds (since {sleep_time})")
        time.sleep(self.delay)

    def run(self):
        while True:
            self.log()
            self.sleep()
        

class SphereLogger(SystemsLogger):
    def __init__(self, center, radius, keys, delay=config.DEFAULT_SLEEP):
        super().__init__(keys, delay=delay)

        self.filename = f"{center} - {radius}ly.json"
        self.systems_data = api.Systems.sphere_systems(center, radius, showAllInfo=1)
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
