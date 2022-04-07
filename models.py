import edsm

# TODO: give each model a dumps() func 
# TODO: Logging
class System():
    """
    arg system_data* <dict>
    
    property stations <Stations>
    property traffic <Traffic>

    attr name <str>
    attr id <int or None>
    attr id64 <int or None>
    attr coords <dict or None>
    attr coordsLocked <bool or None>
    attr requirePermit <bool or None>
    attr information <dict or None>
    attr primaryStar <dict or None>

    Models an individual system
    """
    def __init__(self, system_data:dict):
        self.__dict__ = system_data

        # NOTE: depends on assignment to self.__dict__ to define self.name
        self.stations = Stations(self.name)
        self.traffic = Traffic(self.name)


class Traffic():
    """
    arg system_name* <str> - name of system 
    
    property traffic <dict>
    property breakdown <dict>

    method update

    Models response from EDSM System/traffic endpoint.
    Downstream of <System> objects.
    """
    def __init__(self, system_name:str):
        self.system_name = system_name
        self._traffic = None

    
    @property
    def traffic(self) -> dict:
        if self._traffic == None:
            self.update()

        return self._traffic['traffic']

    @property
    def breakdown(self) -> dict:
        return self._traffic['breakdown']

    def update(self) -> None:
        self._traffic = edsm.System.traffic(self.system_name)

    def dumpdict(self) -> dict:
        return {'traffic' : self.traffic, 'breakdown' : self.breakdown}


class Stations():
    """
    arg system_name* <str> - name of system

    property stations <list>
    property stations_by_name <dict>

    method get_station <Station or None>
        arg station_name* <str>

    method update

    Models response from EDSM System/stations endpoint
    Direct downstream of <System> objects.
    """

    def __init__(self, system_name):
        self.system_name = system_name
        self._stations = None

    @property
    def stations_by_name(self) -> dict:
        return dict(map(lambda s: (s.name, s), self.stations))

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
        stations = edsm.System.stations(self.system_name)
        # wrap each station obj with <Station>
        self._stations = list(map(lambda s: Station(s), stations['stations']))

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
    Direct downstream of <Stations> objects.
    """
    def __init__(self, station_data:dict):
        self.__dict__ = station_data
        self._market = None 

    def __repr__(self):
        # NOTE: depends on assignment to self.__dict__ to define self.name and self.haveMarket
        return f'<{self.__module__}.{self.__class__.__name__}(name="{self.name}", haveMarket={self.haveMarket})>'

    @property
    def market(self) -> 'Market' or None:
        if self.haveMarket and self._market == None:
            self.update_market()

        return self._market

    def update_market(self):
        market_data = edsm.System.marketById(self.marketId)
        self._market = Market(market_data)


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
    Direct downstream of <Station> objects
    """
    def __init__(self, market_data):
        self.__dict__ = market_data
        
        # TODO: model commodities
        # TODO: update method?
