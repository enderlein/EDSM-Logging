import edsm
"""
MODEL class System:
        a container for objs traffic, stations, market, and factions
    __init__(self, query)
        self._query = query
        self.name = 
        self._traffic = None
        self._stations = None -- array of station objs. station objs will hold Market obj
        self._factions = None

        each will hold .update() to fetch new data from API
"""

# TODO: Annotate properties so it's return value's format is clear
# TODO: Finish writing System model, will have to add System endpoint first
class System():
    def __init__(self, system_name):
        self._name = system_name
        self._data = None

        self.populate()

    def populate(self):
        self.bodyCount = d['']

    @property
    def stations(self):
        pass

    @property
    def traffic(self):
        pass

class Stations():
    """
    Models response from EDSM System/stations endpoint
    """

    def __init__(self, system_name):
        self.system_name = system_name
        self._stations = None
        # does not contain a self.populate() because most of the data in EDSM System/stations response
        # is already represented in <System> object

    @property
    def stations(self):
        if self._stations == None:
            d = edsm.System.stations(self.system_name)

            self._stations = list(map(lambda station_data: Station(station_data), d['stations']))

        return self._stations

    def update(self):
        d = edsm.System.stations(self.system_name)
        self._stations = list(map(lambda station_data: Station(station_data), d['stations']))

class Station():
    """
    Models individual station objects in array received in response from EDSM System/stations endpoint
    """
    def __init__(self, station_data):
        self._market = None

        self.populate(station_data)

    def populate(self, d):
        self.id = d['id']
        self.marketId = d['marketId']
        self.type = d['type']
        self.name = d['name']
        self.distanceToArrival = d['distanceToArrival']
        self.allegiance = d['allegiance']
        self.government = d['government']
        self.economy = d['economy']
        self.secondEconomy = d['secondEconomy']
        self.haveMarket = d['haveMarket']
        self.haveShipyard = d['haveShipyard']
        self.haveOutfitting = d['haveOutfitting']
        self.otherServices = d['otherServices']
        self.updateTime = d['updateTime']

    @property
    def market(self):
        if self._market == None:
            market_data = edsm.System.marketById(self.marketId)
            self._market = Market(market_data)

        return self._market

class Market():
    def __init__(self, market_data):
        self.populate(market_data)

    def populate(self, d):
        self.id = d['id']
        self.id64 = d['id64']
        self.name = d['name']
        self.marketId = d['marketId']
        self.sId = d['sId']
        self.sName = d['sName']
        self.commodities = d['commodities']

class Traffic():
    """
    Models response from EDSM System/traffic endpoint
    """
    def __init__(self, system_name):
        self.system_name = system_name
        self._traffic = None

    
    @property
    def traffic(self):
        if self._traffic == None:
            self._traffic = edsm.System.traffic(self.system_name)

        return self._traffic

    @property
    def total(self):
        return self.traffic['traffic']['total']

    @property
    def week(self):
        return self.traffic['traffic']['week']

    @property
    def day(self):
        return self.traffic['traffic']['day']

    @property
    def breakdown(self):
        return self.traffic['breakdown']

    def update(self):
        self._traffic = edsm.System.traffic(self.system_name)

