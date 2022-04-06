import json
import time

from concurrent.futures import ThreadPoolExecutor

import models
import edsm
import config

# TODO: Import config with from calls (not that big a module, but less overhead anyways)
# TODO: Logs should be grouped. As is, data is saved as a bunch of loose json objects. 
# They should be bundled by timestamp. to make comparison easier.
# TODO: logging

# TODO: ABCs lol
class SystemsLogger():
    def __init__(self, keys):
        self.keys = keys

        self._systems = None

        # to be overwritten by children (TODO: ABCs lol)
        self.filename = f'{self}.json'
        self.systems_data = None

    @property
    def systems(self):
        if not self._systems:
            # Wrap system objs from query with models.System objects
            self._systems = list(map(lambda d: models.System(d), self.systems_data))

        return self._systems

    def parse_key(self, obj, key):
        if isinstance(obj.__dict__[key], models.Traffic):
            return obj.__dict__[key].dumpdict()

        return obj.__dict__[key]

    def gather_keys(self, system):
        # creates dict of format {k : self.parse_key(system, k) for k in self.keys}
        return dict(map(lambda k: (k, self.parse_key(system, k)), self.keys))

    def update_by_keys(self):
        # TODO: Find a better way to toggle these.
        if 'traffic' in self.keys:
            self.update_traffic()

        if 'stations' in self.keys:
            self.update_stations()

    def update_traffic(self):
        with ThreadPoolExecutor(max_workers = config.MAX_THREADS) as executor:
            for system in self.systems:
                executor.submit(system.traffic.update)

    def update_stations(self):
        with ThreadPoolExecutor(max_workers = config.MAX_THREADS) as executor:
            for system in self.systems:
                executor.submit(system.stations.update)
        
    def append_file(self, file, data):
        with open(file, 'a') as f:
            f.write(data + '\n')

    def log(self):
        
        self.update_by_keys()

        timestamp = int(time.time())

        for system in self.systems:
            # TODO: Rework output format, group by timestamp
            # TODO: Generalize as generate_json() and write_json() methods
            # so it's easier to implement other output formats (i.e csv)
            payload = self.gather_keys(system)

            payload['timestamp'] = timestamp
            
            s = json.dumps(payload)
            self.append_file(self.filename, s)
        

class SphereLogger(SystemsLogger):
    def __init__(self, center, radius, keys):
        super().__init__(keys)

        self.filename = f"{center} - {radius}ly.json"
        self.systems_data = edsm.Systems.sphere_systems(center, radius, showAllInfo=1)
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
