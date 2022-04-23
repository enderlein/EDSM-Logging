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
"""
 TODO: As of now, resulting .json files are kinda large, find ways to save on space.

        --- Too many timestamps - you're timestamping every single system obj, very redundant you should wrap each
                                   response as an object.

"""
# TODO: ABCs lol
# 
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
    def __init__(self, keys:list[str], delay:int=config.DEFAULT_SLEEP):
        self.keys = keys
        self.delay = delay

        self._systems = None

        # to be overwritten by children (TODO: ABCs lol)
        self.filename = f'{self}.json'
        self.systems_data = None

        # TODO: add check_keys method to make sure provided keys are expected format
        # NOTE: no data is saved if an exception is thrown in the middle of running updates (self.update_by_keys)
        # so it is very important that provided keys are clean and parseable BEFORE running updates. 

    @property
    def systems(self) -> list[models.System]:
        if not self._systems:
            # list[models.System(d) for d in self.systems_data]
            self._systems = list(map(lambda d: models.System(d), self.systems_data))

        return self._systems

    def grab_key(self, obj:models.System, key:Union[str, int]) -> Any:
        # method for grabbing data from <models.System> objects 
        # TODO: Add support for grabbing individual stations with keys formatted like "stations[Ray Hub]"

        excepts = (models.Traffic, models.Stations)

        if isinstance(obj.__dict__[key], excepts):
            return obj.__dict__[key].dumpdict()

        return obj.__dict__[key]

    def gather_by_keys(self) -> list[dict]:
        print("Gathering data by keys")
        # creates a list of dicts containing system data indicated by self.keys
        #TODO: implement passing keys as a model dict instead of as a list.
        # list[dict{k : self.parse_key(system, k) for k in self.keys} for system in self.systems]
        return list(map(lambda system: dict(map(lambda k: (k, self.grab_key(system, k)), self.keys)), self.systems))

    def update_by_keys(self):
        print("Running updates...")
        # update depending on which keys are needed
        # TODO: Find a better way to toggle these, maybe a dict with keys tied to update calls
        if 'traffic' in self.keys:
            self.update_traffic()

        if 'stations' in self.keys:
            self.update_stations()
            # TODO: make market updates optional somehow
            self.update_stations_markets()

        else:
            print("No updates to run")

    def update_traffic(self):
        print("Updating traffic...")
        # Update all <Traffic> objects using :config.MAX_THREADS: workers
        with ThreadPoolExecutor(max_workers = config.MAX_THREADS) as executor:
            for system in self.systems:
                executor.submit(system.traffic.update)

    def update_stations(self):
        print("Updating stations.....")
        # Update all <Stations> objs (attr of <Systems> objs in self.systems) using :config.MAX_THREADS: workers
        with ThreadPoolExecutor(max_workers = config.MAX_THREADS) as executor:
            for system in self.systems:
                executor.submit(system.stations.update)

    def update_stations_markets(self):
        # Update data for all <Market> objs (attr of <Stations> objs) using :config.MAX_THREADS: workers
        print("Updating station markets........")
        with ThreadPoolExecutor(max_workers=config.MAX_THREADS) as executor:
            for system in self.systems:
                for station in system.stations.stations:
                    executor.submit(station.update_market)

    def generate_payload(self):
        print("Generating payload")

        timestamp = int(time.time())
        data = self.gather_by_keys()

        # TODO: Model as class?
        return [{'timestamp' : timestamp, 'data' : data}]

    
    #TODO: Change name to specify that it is appending an array (maybe append_json_array())
    def append_json(self, file:str, data:list[dict]):
        # expecting data from file to be parseable as json array
        # default old_data to empty list if given file doesn't exist or has invalid json (really only want to check for empty files, 
        # should stop/throw warning if there is data but its not valid json. TODO: narrow second exception)
        print(f"Writing to {self.filename}...")
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
        print("Starting routine...")
        # Timestamps and dumps captured data as json to file :<self>.filename:
        #TODO: reorganize above methods so that it's easier to follow program flow
        self.update_by_keys()
        
        payload = self.generate_payload()
        self.append_json(self.filename, payload)
    
    def sleep(self):
        # TODO: Replace print with logging event
        sleep_time = time.strftime("%H:%M:%S", time.localtime())
        print(f"{self} :SLEEPING: for {self.delay} seconds (since {sleep_time})")
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
