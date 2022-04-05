import json
import time
import inspect

from concurrent.futures import ThreadPoolExecutor

import models
import edsm
import config
# TODO: Import config with from calls (not that big a module, but less overhead anyways)
# TODO: Logs should be grouped. As is, data is saved as a bunch of loose json objects. 
# They should be bundled by timestamp. to make comparison easier.
class SystemsLogger():
    def __init__(self, center, radius, delay, keys):
        self.filename = f'{center}_{radius}ly.data' # TODO: there are better options for filename generation
        self.keys = keys

        self._systems_data = None
        self._systems = None

        # TODO: bad to have here, not general properties.
        # center and radius should be defined in Child classes (where needed)
        self.center = center
        self.radius = radius
        self.delay = delay

    @property
    def systems(self):
        # Wrap objs from query data with models.System objects
        # TODO: System objs should be persistent, not generated on the fly
        if not self._systems:
            self._systems = list(map(lambda d: models.System(d), self._systems_data))

        return self._systems

    def gather_keys(self, system):
        # creates dict of format {k : <System>.__dict__[k]} for k in keys
        #d = dict(map(lambda k: (k, system.__dict__[k]), keys))
        d = {}

        for key in self.keys:
            # TODO: add conditional for models.Stations objects
            if isinstance(system.__dict__[key], models.Traffic):
                d[key] = system.__dict__[key].dumpdict()

            else:
                d[key] = system.__dict__[key]
   
        return d

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

    def run(self):
        while True:
            self.update_traffic()
            #self.update_stations()

            timestamp = int(time.time())

            for system in self.systems:
                payload = self.gather_keys(system)

                payload['timestamp'] = timestamp
                
                s = json.dumps(payload)
                self.append_file(self.filename, s)
            
            sleep_time = time.strftime("%H:%M:%S", time.localtime())
            print(f"{self} :Sleeping: for {self.delay} seconds (since {sleep_time})")

            time.sleep(self.delay)

class SphereLogger(SystemsLogger):
    def __init__(self, center, radius, delay, keys):
        super().__init__(center, radius, delay, keys)
        self._systems_data = edsm.Systems.sphere_systems(self.center, self.radius, showAllInfo=1)
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
