import edsm.api as api

# TODO: Logging

# NOTE: 'json_dump' methods are meant to return a json-serializable representation of each model with redundant info removed
# NOTE: 'get_keys' methods are meant allow capturing specific attirbutes returned in 'json_dump' methods

# TODO: automate getting rid of redundancies in output (i.e. system name is listed in system, traffic, and station data)
# TODO: create container model for <System> objects. Can hold get, set, remove logic (as opposed to having to do that in log.py)

class Systems():
    # Container for <System>, (will have the threading logic seen in edsm/log.py)
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
    
    # TODO: come up with tests for update funcs
    def update_traffic(self):
        pass

    def update_stations(self):
        pass

    def get_keys(self):
        pass

    def json_dump(self):
        pass


class System():
    """
    Models individual system objects received from EDSM Systems/* endpoints

    arg: system_data* <dict> - a dict containing system data 
    returned from call to edsm.api.Systems.*
    
    property: stations <Stations>\ 
    property: traffic <Traffic> TODO: update this docstring 

    method: get_keys (keys) <dict>
        arg: keys* <list<dict>>

    attr: name <str>\ 
    attr: id <int or None>\ 
    attr: id64 <int or None>\ 
    attr: coords <dict or None>\ 
    attr: coordsLocked <bool or None>\ 
    attr: requirePermit <bool or None>\ 
    attr: information <dict or None>\ 
    attr: primaryStar <dict or None>
    """
    def __init__(self, system_data:dict):
        # TODO: needs harder typing, system_data should always be a dict, no exceptions
        self.__dict__ = system_data

        # NOTE: depends on assignment to self.__dict__ to define self.name
        # TODO: conditionals for assigning these??? so we're not wasting time initializing these if theyre not needed
        self.stations = Stations(self.name)
        self.traffic = Traffic(self.name)

    def get_keys(self, keys: list[str]):
        return {key : self.__dict__[key] for key in keys}


class Traffic():
    """
    Models response from EDSM System/traffic endpoint.
    Child of <System> objects.

    arg: system_name* <str> - name of system 

    method: update <None> - populates 

    property: daat
    """
    def __init__(self, system_name:str):
        self.system_name = system_name
        self.traffic = None

    def update(self) -> None:
        self.traffic = api.System.traffic(self.system_name)

    def json_dump(self) -> dict:
        if self.traffic:
            return {'traffic' : self.traffic['traffic'], 'breakdown' : self.traffic['breakdown']}

        return None

    def get_keys(self, keys: list[str]): # TODO: raises TypeError when traffic data hasn't been updated. Let user know they need to update first.
        return {key : self.json_dump()[key] for key in keys}


class Stations():
    """
    Models response from EDSM System/stations endpoint.
    Direct child of <System> objects.

    arg: system_name* <str> - name of system

    property: stations <list>\ 
    property: stations_by_name <dict>

    method: get_station(station_name) <Station or None>
        arg: station_name* <str>

    method: update <None>
    """
    def __init__(self, system_name):
        self.system_name = system_name
        self.stations = None

    def __getitem__(self, key:str) -> 'Station' or None:
        if self.stations:
            for station in self.stations:
                if station.name == key:
                    return station
            
        return None

    def __iter__(self):
        if self.stations:
            return iter(self.stations)
        return None # TODO: maybe something should be raised here

    def update(self):
        stations = api.System.stations(self.system_name)
        self.stations = [Station(s) for s in stations['stations']]

    def json_dump(self) -> list:
        return [station.json_dump() for station in self.stations]

    def get_keys(self, keys: list[str]):
        return [{key : station.json_dump()[key] for key in keys} for station in self.stations]


class Station():
    """
    arg station_data* <dict>

    attr id <int>
    attr marketId <int>
    attr type <int>
    attr name <str>
    attr distanceToArrival <int>
    attr allegiance <str>
    attr government <str>
    attr economy <str>
    attr secondEconomy <str>
    attr haveMarket <bool>
    attr haveShipyard <bool>
    attr haveOutfitting <bool>
    attr otherServices <list>
    attr updateTime <dict>

    property market <Market or None>

    Models individual station objects from array received in response from EDSM System/stations endpoint.
    Direct child of <Stations> objects.
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
    arg market_data* <dict>

    attr id <int> - system ID
    attr id64 <int> - system ID64
    attr name <str> - system name
    attr marketId <int>
    attr sId <int> - station ID
    attr sName <str> - station name
    attr commodities <dict>

    Models station market data.
    Direct chiild of <Station> objects
    """
    def __init__(self, market_data):
        self.__dict__ = market_data
        
        # TODO: model commodities
        # TODO: update method?
