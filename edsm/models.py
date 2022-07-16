from concurrent.futures import ThreadPoolExecutor, wait, Future
from typing import Callable

import edsm.api as api
import edsm.config as config
# TODO: Logging

# NOTE: 'json_dump' methods are meant to return a json-serializable representation of each model with redundant info removed
# NOTE: 'get_keys' methods are meant allow capturing specific attirbutes returned in 'json_dump' methods

# TODO: automate getting rid of redundancies in output (i.e. system name is listed in system, traffic, and station data)

class Systems():
    """
    Dict-like container class for <System> objects.

    Threads updates.
    """

    def __init__(self):
        self.list = []
        
    def __delitem__(self, key):
        self.list.remove(self.get(key))

    def __getitem__(self, key:str):
        for item in self.list:
            name = item.__dict__.get('name')
            if name and (name == key):
                return item
        
        else:
            raise KeyError(f"No system with name \'{key}\'")
    
    def __iter__(self):
        return iter(self.list)
        
    def get(self, key:str):
        # Returns star system with given name, returns None if not found
        try:
            r = self[key]
            return r

        except KeyError:
            return None

    def add_system(self, system_data:dict):
        # appends system data (dict) to self.systems
        self.list.append(System(system_data))

    def remove(self, system_name:str):
        try:
            del self[system_name]
        
        # NOTE: not excepting KeyError because ValueError from call to del eats KeyError from call to self[bad_key]
        except ValueError:
            pass

    @staticmethod
    def submit_updates(executor:ThreadPoolExecutor, tasks:list[Callable[[None], None]]):
        futures = []
        for task in tasks:
            future = executor.submit(task)
            futures.append(future)

        return futures

    @staticmethod
    def check_futures(futures:list[Future]):
        wait(futures)
        
        for future in futures:
            if future.exception():
                raise future.exception()

    # TODO: come up with tests for update funcs
    def update_traffic(self):
        with ThreadPoolExecutor(max_workers = config.MAX_THREADS) as executor:
            futures = self.submit_updates(executor, [system.traffic.update for system in self.list])
            self.check_futures(futures)

    def update_stations(self):
        with ThreadPoolExecutor(max_workers = config.MAX_THREADS) as executor:
            futures = self.submit_updates(executor, [system.stations.update for system in self.list])
            self.check_futures(futures)

    def update_stations_markets(self):
        with ThreadPoolExecutor(max_workers=config.MAX_THREADS) as executor:
            tasks = []
            for system in self.list:
                for station in system.stations.list: # NOTE: no comprehension because 2+layer comps are confusing
                    tasks.append(station.update_market)

            futures = self.submit_updates(executor, tasks)
            self.check_futures(futures)

    def get_keys(self, keys_dict:dict[str, list[str]]):
        payload = []

        #TODO: not dynamic. a more 'dynamic' implementation would 'know' all possible keys and what to do with them. 
            # or refer to another obj that 'knows'. 

        for system in self.list:
            d = {}

            for k, keys_list in keys_dict.items():
                # keybinds[k].get_keys(keys_dict[k])
                if k == 'system':
                    d[k] = system.get_keys(keys_list)

                if k == 'traffic':
                    d[k] = system.traffic.get_keys(keys_list)

                if k == 'stations':
                    d[k] = system.stations.get_keys(keys_list)
                

                payload.append(d)

        return payload

    def json_dump(self):
        return [
                    {
                        'system' : system.json_dump(), 
                        'traffic' : system.traffic.json_dump(), 
                        'stations' : system.stations.json_dump()
                    }   for system in self.list
                ]



class System():
    """
    Models individual system objects received from EDSM Systems/* endpoints

    arg: system_data* <dict> - a dict containing system data 
    returned from call to edsm.api.Systems.*
    
    property: stations <Stations>
    property: traffic <Traffic>

    method: json_dump <dict or None>
    method: get_keys (keys) <dict or None>
        arg: keys <list[str]>

    attr: name <str>
    attr: id <int or None>
    attr: id64 <int or None>
    attr: coords <dict or None>
    attr: coordsLocked <bool or None>
    attr: requirePermit <bool or None>
    attr: information <dict or None>
    attr: primaryStar <dict or None>
    """
    def __init__(self, system_data:dict):
        # TODO: needs harder typing, system_data should always be a dict, no exceptions
        self.__dict__ = system_data.copy()
        self.data = system_data

        # NOTE: depends on assignment to self.__dict__ to define self.name. Maybe a bad idea?
        # TODO: conditionals for assigning these??? so we're not wasting time initializing these if theyre not needed
        self.stations = Stations(self.name)
        self.traffic = Traffic(self.name)

    def get_keys(self, keys: list[str]):
        return {key : self.data[key] for key in keys}

    def json_dump(self):
        return self.data


class Traffic():
    """
    Models response from EDSM System/traffic endpoint. 
    Child of <System> objects.

    arg: system_name* <str> - name of system

    property: dict <dict or None>

    method: update <None>
    method: json_dump <dict or None>

    method: get_keys (keys) <dict or None>
        arg: keys <list[str]>
    
    attr: traffic <dict>
    attr: breakdown <dict>

    TODO: doc rest of attributes from api response
    """
    def __init__(self, system_name:str):
        self.system_name = system_name
        self.dict = None

    def update(self) -> None:
        self.dict = api.System.traffic(self.system_name)
        self.__dict__ = self.dict.copy()
        
    def json_dump(self) -> dict:
        if self.dict:
            return {'traffic' : self.dict['traffic'], 'breakdown' : self.dict['breakdown']}

        return None

    def get_keys(self, keys: list[str]):
        if self.dict:
            return {key : self.json_dump()[key] for key in keys}

        # TODO: log warning to tell user that func will return None until corresponding obj is updated (populated with api data)
        return None


class Stations():
    """
    Models response from EDSM System/stations endpoint.
    Direct child of <System> objects.

    arg: system_name* <str> - name of system

    property: list <list> - list of contained stations

    method: update <None>
    method: json_dump <dict or None>

    method: get_keys (keys) <dict or None>
        arg: keys <list[str]>

    TODO: doc attributes from api response
    """
    def __init__(self, system_name):
        self.system_name = system_name
        self.list = None

    def __getitem__(self, key:str) -> 'Station' or None:
        if self.list:
            for station in self.list:
                if station.name == key:
                    return station
            
            else:
                raise KeyError(f"No station found with name {key}")

    def __iter__(self):
        if self.list:
            return iter(self.list)
        return None # TODO: maybe something should be raised here

    def update(self):
        stations = api.System.stations(self.system_name)
        self.list = [Station(s) for s in stations['stations']]

    def json_dump(self) -> list:
        if self.list:
            return [station.json_dump() for station in self.list]

        return None

    def get_keys(self, keys: list[str]):
        if self.list:
            return [{key : station.json_dump()[key] for key in keys} for station in self.list]

        return None


class Station():
    """
    Models individual station objects from array received in response from EDSM System/stations endpoint.
    Direct child of <Stations> objects.

    arg: station_data* <dict>

    property: market <Market or None>

    method: json_dump <dict>
    
    attr: id <int>
    attr: marketId <int>
    attr: type <int>
    attr: name <str>
    attr: distanceToArrival <int>
    attr: allegiance <str>
    attr: government <str>
    attr: economy <str>
    attr: secondEconomy <str>
    attr: haveMarket <bool>
    attr: haveShipyard <bool>
    attr: haveOutfitting <bool>
    attr: otherServices <list>
    attr: updateTime <dict>
    """
    def __init__(self, station_data:dict):
        self.__dict__ = station_data
        self.market = None 

    def __repr__(self):
        # NOTE: depends on above assignment to self.__dict__ to define self.name and self.haveMarket
        return f'<{self.__module__}.{self.__class__.__name__}(name="{self.name}", haveMarket={self.haveMarket})>'

    def update_market(self):
        if self.haveMarket:
            market_data = api.System.marketById(self.marketId)
            self.market = Market(market_data)

    def json_dump(self) -> dict:
        dict_copy = self.__dict__.copy()
        del dict_copy['market'] # deleting because held <Market> obj is not json serializable. 
        
        dict_copy.update({'market' : self.market.commodities if self.market else None})
        return dict_copy

    # TODO: add get_key maybe


class Market():
    """
    arg: market_data* <dict>

    attr: id <int> - system ID
    attr: id64 <int> - system ID64
    attr: name <str> - system name
    attr: marketId <int>
    attr: sId <int> - station ID
    attr: sName <str> - station name
    attr: commodities <dict>

    Models station market data.
    Direct chiild of <Station> objects
    """
    def __init__(self, market_data):
        self.__dict__ = market_data
        
        # TODO: model commodities?
        # TODO: update method?
