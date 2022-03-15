import time
from concurrent.futures import ThreadPoolExecutor

import config
import edsm

# TODO: Write tests


class TrafficNetwork():
    def __init__(self, *systems):
        self.monitors = {}
        self.init_monitors(systems)
        
    def init_monitors(self, systems):
        monitors = []
        for name in systems:
            m = edsm.traffic(name)
            monitors.append(m)

        return monitors


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

    def update_monitors(self):
        with ThreadPoolExecutor(max_workers=config.MAX_THREADS) as executor:
            for monitor in self.monitors.values():
                executor.submit(monitor.update)
    
    def add_monitor(self, name):
        monitor = TrafficMonitor(name)
        self.monitors[monitor.name] = monitor

    def get_monitor(self, name):
        return self.monitors[name]

    def update_monitor(self, name):
        self.monitors[name].update()


class TrafficMonitor():
    def __init__(self, query):
        self._traffic = None
        self._last = None

        self.update()

        self.name = self.traffic['system_name']

    @property
    def diff(self):
        if self._traffic == None or self._last == None:
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

    @property
    def traffic(self):
        if not self._traffic:
            self._traffic = self.fetch_traffic()

        return self._traffic

    def fetch_traffic(self):
        t = edsm.traffic(self.name)
        d = {'system_name' : t['name'],
                'traffic' : t['traffic'],
                'breakdown' : t['breakdown'],
                'timestamp' : int(time.time())}

        return d

    def update(self):
        self._last = self._traffic
        self._traffic = self.fetch_traffic()
