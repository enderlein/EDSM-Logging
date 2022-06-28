import edsm.api as api

# TODO: Logging

# TODO: REDO All of these models
    
# TODO: as of now just manually formatting models to remove redundant attributes from json output
# find a more automatic way to do this (remove values from lower-nested objs if identical value found in higher-nested obj?)

# TODO: work parse_key method into Stations and Traffic model
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
        self.__dict__ = system_data

        # NOTE: depends on assignment to self.__dict__ to define self.name
        # TODO: conditionals for assigning these???
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
    """
    def __init__(self, system_name:str):
        self.system_name = system_name
        self._traffic = None

    def update(self) -> None:
        self._traffic = api.System.traffic(self.system_name)

    def data(self) -> dict:
        # NOTE: using underscored vars here to avoid unwanted calls to self.update() during
        # calls to self.data()
        if self._traffic:
            return {'traffic' : self._traffic['traffic'], 'breakdown' : self._traffic['breakdown']}

        return None

    def get_keys(self, keys: list[str]): # TODO: raises TypeError when traffic data hasn't been updated. Let user know they need to update first.
        return {key : self.data()[key] for key in keys}


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
        self._stations = None

    # TODO: consider removing this entire model, stations can just be wrapped in a list
    # and search logic can be handled by System object
    @property
    def stations_by_name(self) -> dict:
        # dict{s.name : s for s in self.stations}
        return dict(map(lambda s: (s.name, s), self.stations))

    # TODO: rename to 'list' (so that calls are formed like system.stations.list)
    @property
    def stations(self) -> list:
        if self._stations == None:
            self.update()

        return self._stations

    def get_station(self, station_name:str) -> 'Station' or None:
        try:
            return self.stations_by_name[station_name]
        except KeyError:
            return None

    def update(self):
        stations = api.System.stations(self.system_name)
        # list[Station(s) for s in stations['stations']] # TODO
        self._stations = list(map(lambda s: Station(s), stations['stations']))

    def data(self): # TODO: rename to 'data' 
        # NOTE: Using
        # list[station.data() for station in stations] # TODO
        return list(map(lambda s: s.data(), self._stations))

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
        self._market = None 

    def __repr__(self):
        # NOTE: depends on above assignment to self.__dict__ to define self.name and self.haveMarket
        return f'<{self.__module__}.{self.__class__.__name__}(name="{self.name}", haveMarket={self.haveMarket})>'

    @property
    def market(self) -> 'Market' or None:
        if self._market == None:
            self.update_market()

        return self._market

    def update_market(self):
        if self.haveMarket:
            market_data = api.System.marketById(self.marketId)
            self._market = Market(market_data)

    def data(self): # TODO: rename to 'data'
        d = self.__dict__.copy()
        del d['_market'] # deleting because held <Market> obj is not json serializable. 
        
        #TODO: I wanted to re-format this conditional here. I don't remember how I wanted to do that, though
        # or why
        return {'station' : d, 'market' : self._market.__dict__ if self._market else None}


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
