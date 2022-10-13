import edsm.log
import edsm.api
import json

# Indicate which pieces of data to capture from which EDSM API endpoints by
# building a dict with class names as keys and model attribute names as corresponding values
# See docstrings under System(), Traffic(), and Station() classes in models.py for possible attribute names.
keys = {'system' : ['name', 'coords'], 'traffic' : ['traffic', 'breakdown']}
# keys = {'system' : ['name', 'id', 'coords', 'information'], 'traffic' : ['traffic', 'breakdown'], 'stations' : ['name', 'economy', 'market']}

# create Logger object using keys
logger = edsm.log.Logger(keys = keys)

# set filename to 'test.json' (optional)
logger.filepath = 'test.json'

# query edsm.net for star systems within 8 ly of star system 'Sol'
sphere_data = edsm.api.Systems.sphere_systems('Sol', radius = 8, showCoordinates=True)

# populate <edsm.log.Logger>.systems with API data
logger.systems.populate(sphere_data)

# get and append requested data to file, creates file if it doesn't exist
logger.log()

"""***"""

# Doing some stuff to the data
MIN_TRAFFIC = 5
with open(logger.filepath, 'r') as f:
    datalog = json.loads(f.read())

    for item in datalog:
        print(item['timestamp'])

        for entry in item['data']:
            traffic_count = entry['traffic']['traffic']['day']

            if traffic_count >= MIN_TRAFFIC:
                print(f"\t{entry['system']['name']} : {traffic_count}")
