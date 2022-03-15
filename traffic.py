import time
from concurrent.futures import ThreadPoolExecutor

import config
import edsm

# TODO: Write tests
# TODO: add Link model to join multiple system updates together

class TrafficNetwork():
    '''
    <TrafficNetwork>.monitors ( dict{str : <TrafficMonitor>} ) - A dict of <TrafficMonitor> objects with
    associated system names as keys. add_monitor, get_monitor, and update_monitor methods will act on this dict
    '''
    def __init__(self, *system_names):
        self.monitors = {}
        self.init_monitors(list(system_names))
        
    def init_monitors(self, system_names: list) -> None:
        '''
        system_names* (list[str]) - list of system names to create <TrafficMonitor> objects for

        Add multiple <TrafficMonitor> objects to self.monitors using given 
        system names (uses multithreading)
        
        settings:
            config.MAX_THREADS
        '''
        with ThreadPoolExecutor(max_workers=config.MAX_THREADS) as executor:
            for name in system_names:
                executor.submit(self.add_monitor, name)

    def update_monitors(self):
        '''
        Update all monitors in self.monitors (uses multithreading)
        settings:
            config.MAX_THREADS 
        '''
        with ThreadPoolExecutor(max_workers=config.MAX_THREADS) as executor:
            for monitor in self.monitors.values():
                executor.submit(monitor.update)

    def add_monitor(self, name: str) -> None:
        '''
        name* (str) - name of star system to associate with <TrafficMonitor> object
        
        Adds monitor for system with given name to self.monitors
        '''
        monitor = TrafficMonitor(name)
        self.monitors[monitor.name] = monitor

    def get_monitor(self, name: str) -> 'TrafficMonitor':
        '''
        name* (str) - name of star system associated with <TrafficMonitor> object

        returns <TrafficMonitor> object in self.monitors with given name
        '''
        return self.monitors[name]

    def update_monitor(self, name: str) -> None:
        '''
        name* (str) - name of star system associated with TrafficMonitor object

        Updates <TrafficMonitor> object in self.monitors with given name
        '''
        self.monitors[name].update()


class TrafficSphere(TrafficNetwork):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
        self.monitors = {}

        self.init_monitors()

    def init_monitors(self):
        systems = edsm.systems_radius(system_name = self.center, radius = self.radius)
        names = [system['name'] for system in systems]

        with ThreadPoolExecutor(max_workers=config.MAX_THREADS) as executor:
            for name in names:
                executor.submit(self.add_monitor, name)



class TrafficMonitor():
    def __init__(self, name):
        self._query = name
        self._traffic = None
        self._last = None

        self.update()

        self.name = self.traffic['system_name']

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
        t = edsm.traffic(self._query)
        d = {'system_name' : t['name'],
                'traffic' : t['traffic'],
                'breakdown' : t['breakdown'],
                'timestamp' : int(time.time())}

        return d

    def update(self):
        self._last = self._traffic
        self._traffic = self.fetch_traffic()
