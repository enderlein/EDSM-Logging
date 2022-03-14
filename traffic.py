import json
import time

from concurrent.futures import ThreadPoolExecutor

import edsm

# build class TrafficMonitor, use Traffic model to build Traffic monotiring network 
# TODO: TrafficSphere
# TODO: Update on a schedule
# TODO: Cross-reference hour-by-hour traffic data to track players.

# TODO: Write tests
# TODO: add 'diff' method that detects changes in traffic data from last update
class TrafficSphere():
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
        self.monitors = {}

        self.init_monitors()

    def init_monitors(self):
        systems = edsm.systems_radius(system_name = self.center, radius = self.radius)
        for system in systems:
            monitor = TrafficMonitor(system['name'])
            self.monitors[system['name']] = monitor

    def update(self):
        with ThreadPoolExecutor(max_workers=20) as executor:
            for monitor in self.monitors.values():
                executor.submit(monitor.update)

    def update_monitor(self, name):
        self.monitors[name].update()

    def get_monitor(self, name):
        return self.monitors[name]


class TrafficMonitor():
    def __init__(self, name):
        self.name = name
        self._traffic = None

    def fetch_traffic(self):
        t = edsm.traffic(self.name)
        d = {'traffic' : t['traffic'],
            'breakdown' : t['breakdown'],
            'timestamp' : int(time.time())}

        return d

    @property
    def traffic(self):
        if not self._traffic:
            self._traffic = self.fetch_traffic()

        return self._traffic

    def update(self):
        self._traffic = self.fetch_traffic()
