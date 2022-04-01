import edsm

# TODO: Annotate properties so its return value's format is clear
# TODO: Finish writing System model, will have to add System endpoint first
# TODO: Take advantage of __dict__ instead of doing all this nonsense.
# TODO: Start collecting data and consider how you want to use it before you finish bulding
#these models
class System():
    """
    arg system_data* (dict)

    property stations (Stations)
    property traffic (Traffic)

    attr name (str)
    attr id (int or None)
    attr id64 (int or None)
    attr coords (dict or None)
    attr coordsLocked (bool or None)
    attr requirePermit (bool or None)
    attr information (dict or None)
    attr primaryStar (dict or None)

    Models an individual system
    """
    def __init__(self, system_data):
        self.__dict__ = system_data # does what .populate() does but so much nicer

        self.stations = Stations(self.name)
        self.traffic = Traffic(self.name)


class Traffic():
    """
    arg system_name* (str) - name of system 
    
    property data (dict)
    property total (int)
    property week (int)
    property day (int)
    property breakdown (dict)

    method update

    Models response from EDSM System/traffic endpoint.
    Child of <System> objects.
    """
    def __init__(self, system_name):
        self.system_name = system_name
        self._traffic = None

    
    @property
    def traffic(self):
        if self._traffic == None:
            self.update()

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

class Stations():
    """
    arg system_name* (str) - name of system

    property stations (list)

    method get_station (Station)
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

        return list(self._stations.values())

    def get_station(self, station_name):
        return self._stations[station_name]

    def update(self):
        d = edsm.System.stations(self.system_name)
        self._stations = dict(map(lambda station_data: (station_data['name'], Station(station_data)), d['stations']))

class Station():
    """
    arg station_data* (dict)

    attr id (int)
    attr marketId (int)
    attr type (int)
    attr name (str)
    attr distanceToArrival (int)
    attr allegiance (str)
    attr government (str)
    attr economy (str)
    attr secondEconomy (str)
    attr haveMarket (bool)
    attr haveShipyard (bool)
    attr haveOutfitting (bool)
    attr otherServices (list)
    attr updateTime (dict)

    property market

    Models individual station objects in array received in response from EDSM System/stations endpoint.
    Child of <Stations> objects.
    """
    def __init__(self, station_data):
        self.__dict__ = station_data
        self._market = None 

    def __repr__(self):
        return f'<models.Station(name="{self.name}", haveMarket="{self.haveMarket}")>'

    @property
    def market(self):
        if self._market == None:
            market_data = edsm.System.marketById(self.marketId)
            self._market = Market(market_data)

        return self._market


class Market():
    """
    arg market_data* (dict)

    attr id (int)
    attr id64 (int)
    attr name (str)
    attr marketId (int)
    attr sId (int)
    attr sName (str)
    attr commodities (dict)

    Models station market data.
    Child of <Station> objects
    """
    def __init__(self, market_data):
        self.__dict__ = market_data
        
        # TODO: model commodities
        # TODO: update method?
