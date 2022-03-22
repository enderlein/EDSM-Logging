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

class Traffic():
    """
    Models EDSM traffic data
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

