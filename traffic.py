import time
from concurrent.futures import ThreadPoolExecutor

import config
import edsm

# TODO: Write tests
# TODO: Add update queue feature to TrafficNetworks
# TODO: generalize, make new file called models.py, create System model that will contain
# a TrafficMonitor and other _Monitor objects (market, factions for now)

class TrafficNetwork():
    def __init__(self, *system_names):
        '''
        <self>.monitors (dict) - stores <TrafficMonitor> objects in format {<TrafficMonitor>.name : <TrafficMonitor>}. 
                                    init_monitors, update_all, add_monitor, get_monitor, and update_monitor methods will act on this dict
        '''
        self._monitors = {}
        self.init_monitors(list(system_names))

    @property
    def monitors(self):
        return self._monitors.values()
        
    def init_monitors(self, system_names: list) -> None:
        '''
        system_names* (list[str]) - list of system names to create <TrafficMonitor> objects for

        Add multiple <TrafficMonitor> objects to self._monitors using given 
        system names (uses multithreading)
        
        settings:
            config.MAX_THREADS
        '''
        with ThreadPoolExecutor(max_workers=config.MAX_THREADS) as executor:
            for name in system_names:
                executor.submit(self.add_monitor, name)

    def update_all(self) -> None:
        '''
        Update all monitors in self._monitors (uses multithreading)
        settings:
            config.MAX_THREADS 
        '''
        with ThreadPoolExecutor(max_workers=config.MAX_THREADS) as executor:
            for monitor in self._monitors.values():
                executor.submit(monitor.update)

    def add_monitor(self, name: str) -> None:
        '''
        name* (str) - name of star system to associate with <TrafficMonitor> object
        
        Adds monitor for system with given name to self._monitors
        '''
        monitor = TrafficMonitor(name)
        self._monitors[monitor.name] = monitor

    def get_monitor(self, name: str) -> 'TrafficMonitor':
        '''
        name* (str) - name of star system associated with <TrafficMonitor> object

        returns <TrafficMonitor> object in self._monitors with given name
        '''
        return self._monitors[name]

    def update_monitor(self, name: str) -> None:
        '''
        name* (str) - name of star system associated with TrafficMonitor object

        Updates <TrafficMonitor> object in self._monitors with given name
        '''
        self._monitors[name].update()


class TrafficSphere(TrafficNetwork):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

        super().__init__(*self.fetch_systems_radius(self.center, self.radius))

    def fetch_systems_radius(self, center, radius):
        systems = edsm.Systems.sphere_systems(systemName = center, radius = radius)
        names = [system['name'] for system in systems]

        return names


class TrafficMonitor():
    def __init__(self, name):
        self._query = name
        self._traffic = None
        self._last = None
        self.name = None

        self.update()

    @property
    def diff(self):
        if self._traffic == None or self._last == None:
            return None

        else:
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
        t = edsm.System.traffic(self.name if self.name else self._query)
        d = {'system_name' : t['name'],
                'traffic' : t['traffic'],
                'breakdown' : t['breakdown'],
                'timestamp' : int(time.time())}

        return d

    def update(self):
        self._last = self._traffic
        self._traffic = self.fetch_traffic()

        if not self.name:
            self.name = self._traffic['system_name']
