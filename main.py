import json
import time 

from concurrent.futures import ThreadPoolExecutor

import models
import edsm
import config
# TODO: Import config with from calls (not that big a module, but less overhead anyways)

class SphereLogger():
    def __init__(self, center, radius, delay):
        self.filename = f'{center}_{radius}ly.data'
        self.delay = delay
        self.sphere = edsm.Systems.sphere_systems(center, radius, showAllInfo=1)
        self._systems = None

    @property
    def systems(self):
        if not self._systems:
            self._systems = list(map(lambda d: models.System(d), self.sphere))

        return self._systems

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
                payload = {'name' : system.name,
                            'id' : system.id,
                            'id64' : system.id64,
                            'coords' : system.coords,
                            'traffic' : system.traffic.traffic,
                            'breakdown' : system.traffic.breakdown,
                            'timestamp' : timestamp}

                s = json.dumps(payload)
                self.append_file(self.filename, s)
            
            sleep_time = time.strftime("%H:%M:%S", time.localtime())
            print(f"{self} :Sleeping: for {self.delay} seconds (since {sleep_time})")
            time.sleep(self.delay)
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
