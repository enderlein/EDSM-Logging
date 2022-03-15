import json
import warnings
import time

from concurrent.futures import ThreadPoolExecutor

import config
import edsm

# build class TrafficMonitor, use Traffic model to build Traffic monotiring network 
# TODO: TrafficSphere
# TODO: Update on a schedule
# TODO: Cross-reference hour-by-hour traffic data to track players.

# TODO: Write tests

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
        with ThreadPoolExecutor(max_workers=config.MAX_THREADS) as executor:
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
        self._last = None

    @property
    def diff(self):
        if self._last == None:
            warnings.warn("'diff' defaulting to None: Nothing to compare to!")
            return None

        elif self._last != None:
            diff_traffic = {k : self._traffic['traffic'][k] - self._last['traffic'][k] for k in self._traffic['traffic']}
            
            diff_breakdown = {}
            for ship in self._traffic['breakdown']:
                if ship in self._last['breakdown']:
                    diff_breakdown[ship] = self._traffic['breakdown'][ship] - self._last['breakdown'][ship]
                else:
                    diff_breakdown[ship] = self._traffic['breakdown'][ship]

            diff_timestamp = self._traffic['timestamp'] - self._last['timestamp']

            d = {'system_name' : self.name,
                    'traffic' : diff_traffic,
                    'breakdown' : diff_breakdown,
                    'timestamp' : diff_timestamp}

            return d

    def fetch_traffic(self):
        t = edsm.traffic(self.name)
        d = {'system_name' : t['name'],
                'traffic' : t['traffic'],
                'breakdown' : t['breakdown'],
                'timestamp' : int(time.time())}

        return d

    @property
    def traffic(self):
        if not self._traffic:
            self._traffic = self.fetch_traffic()

        return self._traffic

    def update(self):
        self._last = self._traffic
        self._traffic = self.fetch_traffic()
