import edsm.log
import edsm.api

# Indicate which pieces of data to capture from which EDSM API endpoints by
# building a dict with class names as keys and model attribute names as corresponding values
# See docstrings under System(), Traffic(), and Station() classes in models.py for possible attribute names.
keys = {'system' : ['name', 'id', 'coords', 'information'], 'traffic' : ['traffic', 'breakdown'], 'stations' : ['name', 'economy', 'market']}

# create Logger object using keys
logger = edsm.log.Logger(keys = keys)

# Query edsm.net for star systems within 8 ly of star system 'Warkawa'
sphere_data = edsm.api.Systems.sphere_systems('Warkawa', radius = 8, showAllInfo = True)

# populate <edsm.log.Logger>.systems with systems data from sphere_data
for system_data in sphere_data:
    logger.systems.add_system(system_data)

# set filename to 'test.json'
logger.filename = 'test.json'

# gets and appends requested data to file, creates file if it doesn't exist
logger.log()
