import edsm.log
import edsm.api

keys = {'system' : ['name', 'id', 'coords', 'information'], 'traffic' : ['traffic'], 'stations' : ['name', 'economy', 'market']}

logger = edsm.log.Logger(keys = keys)
sphere_data = edsm.api.Systems.sphere_systems('Warkawa', radius = 8, showAllInfo = True)

for system in sphere_data:
    logger.systems.add_system(system)

logger.filename = 'test.json'
logger.log()
