import edsm

# TODO: Annotate properties so its return value's format is clear
# TODO: Finish writing System model, will have to add System endpoint first
class System():
    """
    Models an individual system

    arg system_data* (dict)

    property stations (Stations)
    property traffic (Traffic)
    """
    def __init__(self, system_data):
        self._data = system_data

        self._stations = None
        self._traffic = None

        self.populate(self._data)

    def populate(self, d):

        # successful responses will always show name
        self.name = d['name']

        # TODO: there is probs a better way to default
        self.id = d['id'] if 'id' in d else None
        self.id64 = d['id64'] if 'id64' in d else None
        self.coords = d['coords'] if 'coords' in d else None
        self.coordsLocked = d['coordsLocked'] if 'coordsLocked' in d else None
        self.requirePermit = d['requirePermit'] if 'requirePermit' in d else None
        self.information = d['information'] if 'information' in d else None
        self.primaryStar = d['primaryStar'] if 'primaryStar' in d else None

    @property
    def stations(self):
        if self._stations == None:
            self._stations = Stations(self.name)

        return self._stations

    @property
    def traffic(self):
        if self._traffic == None:
            self._traffic = Traffic(self.name)

        return self._traffic


class Traffic():
    """
    arg system_name* (str) - name of system 
    
    property data
    property total
    property week
    property day
    property breakdown

    method update

    Models response from EDSM System/traffic endpoint.
    Child of <System> objects.
    """
    def __init__(self, system_name):
        self.system_name = system_name
        self._data = None

    
    @property
    def data(self):
        if self._data == None:
            self._data = edsm.System.traffic(self.system_name)

        return self._data

    @property
    def total(self):
        return self.data['traffic']['total']

    @property
    def week(self):
        return self.data['traffic']['week']

    @property
    def day(self):
        return self.data['traffic']['day']

    @property
    def breakdown(self):
        return self.data['breakdown']

    def update(self):
        self._data = edsm.System.traffic(self.system_name)

class Stations():
    """
    arg system_name* (str) - name of system

    property stations

    method get_station
    method update

    Models response from EDSM System/stations endpoint
    Child of <System> objects.
    """

    def __init__(self, system_name):
        self.system_name = system_name
        self._stations = {}
        # does not contain a self.populate() because most of the data in EDSM System/stations response
        # is already represented in <System> object

    @property
    def stations(self):
        if self._stations == {}:
            self.update()

        return self._stations

    def get_station(self, station_name):
        return self.stations[station_name]

    def update(self):
        d = edsm.System.stations(self.system_name)
        self._stations = dict(map(lambda station_data: (station_data['name'], Station(station_data)), d['stations']))

class Station():
    """
    arg station_data* (dict)

    attr id (int)
    attr marketId (int)
    attr type (int)

    property market

    Models individual station objects in array received in response from EDSM System/stations endpoint.
    Child of <Stations> objects.
    """
    def __init__(self, station_data):
        self._market = None

        self.populate(station_data)

    def __repr__(self):
        return f'Station(name="{self.name}", haveMarket="{self.haveMarket}")'

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
    """
    arg market_data* (dict)

    Models station market data.
    Child of <Station> objects
    """
    def __init__(self, market_data):
        self.populate(market_data)

    def populate(self, d):
        self.id = d['id']
        self.id64 = d['id64']
        self.name = d['name']
        self.marketId = d['marketId']
        self.sId = d['sId']
        self.sName = d['sName']
        # TODO: model commodities
        self.commodities = d['commodities']

    # TODO: update method?
